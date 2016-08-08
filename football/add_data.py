# -*- coding: utf-8 -*-
import calendar
import datetime
import hashlib
import json
import os
import sys
import time
import utils
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import sports.project.utils as project_utils
from fetch_data import GetFlagImage, GetStadium
import settings
from interfaces import AddFootballDataInterface
from sports.project.test import A
from sports.project import utils as project_utils
now = datetime.datetime.now()


class AddFootballData(AddFootballDataInterface):

    @staticmethod
    def add_football_leagues():
        url = settings.FOOTBALL_ALL_LEAGUES_URL.format(settings.API_KEY)
        response = requests.get(url)
        data = json.loads(response.content)
        conn = project_utils.get_mongodb_connection()
        new_football_leagues_conn = conn.football.new_football_leagues
        for league in data:
            new_football_leagues_conn.update({'league_id':league['id']},
                                             {'$set':{'league_id':league['id'],
                                                      'league_name':league['name'],
                                                      'region':league['region']}},upsert = True)

    @staticmethod
    def add_league_standings(league_id):
        url = settings.FOOTBALL_LEAGUE_STANDINGS_URL.format(league_id,settings.API_KEY)
        response = requests.get(url)
        data = json.loads(response.content)
        conn = project_utils.get_mongodb_connection()
        football_standings_conn = conn.football.football_standings
        new_football_leagues_conn = conn.football.new_football_leagues
        try:
            for team in data:
                stand_team_name = team['team_name'].encode('utf-8')
                flag_image = GetFlagImage.flag_single(stand_team_name)
                league = list(new_football_leagues_conn.find({'league_id': str(team['comp_id'])}, projection={'_id':False}))
                league_data = league[0]['league_name'] + ',' + league[0]['region']
                football_standings_conn.update({'league_id':team['comp_id'],
                    'team_name':team['team_name'],
                    'stand_season':team['season']},
                    {'$set':{'league_id': team['comp_id'],
                    'stand_season':team['season'],
                    'stand_group':team['comp_group'],
                    'league_name':league_data,
                    'flag_image': flag_image,
                    'position': int(team['position']),
                    'recent_form': team['recent_form'],
                    'team_name': team['team_name'],
                    'team_id': int(team['team_id']),
                    'games_played': team['overall_gp'],
                    'games_won': team['overall_w'],
                    'games_lost': team['overall_l'],
                    'games_drawn':team['overall_d'],
                    'team_points': team['points'],
                    'sport_type':'football'}}, upsert = True)
        except Exception as e:
            print e

    @staticmethod
    def upcoming_fixtures(date=None):
        url = settings.FOOTBALL_UPCOMING_FIXTURES_URL.format(date, settings.API_KEY)
        response = requests.get(url)
        data = json.loads(response.content)
        try:
            print data['status']
        except Exception as e:
            AddFootballData.add_upcoming_fixtures(data)
            return

    @staticmethod
    def todays_fixtures():
        url = settings.FOOTBALL_TODAYS_FIXTURES_URL.format(settings.API_KEY)
        response = requests.get(url)
        data = json.loads(response.content)
        try:
            print data['status'],data['message']
            return False
        except Exception as e:
            AddFootballData.add_upcoming_fixtures(data)
            return

    @staticmethod
    def add_upcoming_fixtures(data):
        conn = project_utils.get_mongodb_connection()
        football_db = conn.football
        new_football_fixtures = football_db.new_football_fixtures
        new_football_leagues = football_db.new_football_leagues
        betfair_odds_db = conn.betfair_odds
        football_odds = betfair_odds_db.football_odds
        try:
            for match in data:
                try:
                    league = list(new_football_leagues.find({'league_id':str(match['comp_id'])},projection={'_id':False}))
                    league_data = league[0]['league_name'] + ',' + league[0]['region']
                    ep_date = calendar.timegm(time.strptime(match['formatted_date'] + match['time'],'%d.%m.%Y%H:%M'))
                    flag_images = GetFlagImage.flag_double(match['localteam_name'], match['visitorteam_name'])
                    if match.get('venue') != '':
                        stadium_name = match.get('venue')
                    else:
                        stadium_name = GetStadium.stadium(match['localteam_name'])
                    odds_value = list(football_odds.find({'team_1':match['localteam_name'],
                                                          'team_2':match['visitorteam_name']},projection={'_id':False}))
                    print odds_value

                    set_dict = {
                        'league_id': int(match['comp_id']),
                        'league_name':league_data,
                        'home_team': match['localteam_name'],
                        'home_team_flag': flag_images[0],
                        'home_team_id':int(match['localteam_id']),
                        'stadium': stadium_name,
                        'away_team': match['visitorteam_name'],
                        'away_team_flag': flag_images[1],
                        'away_team_id':int(match['visitorteam_id']),
                        'match_date_epoch': ep_date,
                        'match_date':match['formatted_date'],
                        'match_id': int(match['id']),
                        'home_team_score': match['localteam_score'],
                        'away_team_score': match['visitorteam_score'],
                        'match_status': match['status'],
                        'match_time': match['time'],
                        'timer':match['timer']
                    }

                    if odds_value:
                        set_dict.update({
                            'team_1_odds':odds_value[0]['team_1_odds'],
                            'team_2_odds':odds_value[0]['team_2_odds'],
                            'draw_odds':odds_value[0]['draw_odds'],
                        })

                    if set_dict['home_team_flag'] and set_dict['away_team_flag']:
                        print set_dict
                        #if flags are availlable then only update data
                        new_football_fixtures.update({'match_id': int(match['id'])},
                                                     {'$set': set_dict }, upsert = True)

                        live_status = False
                        if match['status'] not in [match['time'],'FT','Postp.','Cancl.']:
                            live_status = True

                        new_football_fixtures.update({'match_id':int(match['id'])},
                                                     {'$set':{'live':live_status}},upsert= True)
                        #to update commentary
                        AddFootballData.match_commentary(match['id'], match['events'])

                        result = ''
                        if match['status'] == 'FT':
                            if match['localteam_score'] > match['visitorteam_score']:
                                result = 'home_team'
                            elif match['localteam_score'] < match['visitorteam_score']:
                                result = 'away_team'

                        new_football_fixtures.update({'match_id':int(match['id'])},{'$set':{'result':result}},upsert=True)
                    AddFootballData.match_commentary(match['comp_id'],match['events'])
                except Exception as e:
                    print e
        except Exception as e:
            raise e
        print 'data added'
        return

    @staticmethod
    def match_commentary(match_id, events):
        """
        This actually fetches match commentary from a thir party api
        """
        
        url = settings.FOOTBALL_MATCH_COMMENTARY_URL.format(match_id, settings.API_KEY)
        response = requests.get(url)
        data = json.loads(response.content)
        try:
            print data['status'],data['message']
            return False
        except Exception as e:
            (match_stats, match_subs, match_player_stats, single_match_teams,
             match_substitutions) = utils.get_match_data(data)
            utils.add_match_stats(int(match_id), match_stats)
            utils.add_match_subs(int(match_id), match_subs)
            utils.add_match_summary(int(match_id), events)
            utils.add_players_stats(int(match_id), match_player_stats)
            utils.add_match_teams(int(match_id), single_match_teams)
            utils.add_match_substitutions(int(match_id), match_substitutions)
            utils.add_match_timeline(int(match_id), match_substitutions, events)
            new_comments = utils.add_match_commentary(int(match_id), data['comments'])
            football_notifications.check_event(match_id, new_comments)
            print 'all data added'
        return

    @staticmethod
    def add_team_squads(team_id):
        print team_id
        url = settings.FOOTBALL_TEAM_PROFILE_URL.format(team_id, settings.API_KEY)
        response = requests.get(url)
        data = json.loads(response.content)
        conn = project_utils.get_mongodb_connection()
        team_squad_conn = conn.football.team_squad
        try:
            print data['status'],data['message']
        except Exception as e:
            team_squad_conn.update({'team_id':team_id},
                                   {'$set':{'team_id':team_id,
                                            'players':data['squad'],
                                            'manager':data['coach_name']}},upsert = True)


    @staticmethod
    def update_player_stats(player_id):
        url = settings.FOOTBALL_PLAYER_PROFILE_URL.format(player_id, settings.API_KEY)
        response = requests.get(url)
        data = json.loads(response.content)
        conn = project_utils.get_mongodb_connection()
        player_profile_conn = conn.football.player_profile
        player_profile_conn.update({'player_id':data['id']},
                                   {'$set':{'player_id':data['id'],
                                            'name':data['name'],
                                            'firstname':data['firstname'],
                                            'lastname':data['lastname'],
                                            'team':data['team'],
                                            'team_id':data['teamid'],
                                            'position':data['position'],
                                            'nationality':data['nationality'],
                                            'age':data['age'],
                                            'birthplace':data['birthplace'],
                                            'weight':data['weight'],
                                            'height':data['height'],
                                            'birthdate':data['birthdate'],
                                            'birthcountry':data['birthcountry'],
                                            'player_stats':data['player_statistics']}},upsert = True)

