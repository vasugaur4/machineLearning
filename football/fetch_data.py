# -*- coding: utf-8 -*-

import calendar
import datetime
import operator
import os
import sys
import time


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from interfaces import GetFootballDataInterface, BaseFlagImageHandler, BaseStadiumHandler
import settings
import sports.project.utils as project_utils

now = datetime.datetime.now()

# GET MONGO_CONNECTION HERE

conn = project_utils.get_mongodb_connection()

DB = conn.football
new_football_leagues_conn = DB.new_football_leagues
football_standings_conn = DB.football_standings
football_players_conn = DB.players_db
new_football_fixtures_conn = DB.new_football_fixtures
match_statistics_conn = DB.match_statistics
match_teams_conn = DB.match_teams
match_substitutes_conn = DB.match_substitutes
match_substitutions_all_conn = DB.match_substitutions_all
football_timeline_conn = DB.football_timeline
player_stats_conn = DB.player_stats
match_summ_conn = DB.match_summ
players_db_conn = DB.players_db
football_comm_conn = DB.football_comm
team_squad_conn = conn.football.team_squad
player_profile_conn = conn.football.player_profile


class FootBallData(GetFootballDataInterface):

    @staticmethod
    def get_leagues():
        """
        :return: list of all football leagues.
        """
        new_football_leagues = list(new_football_leagues_conn.find(projection = {'_id' : False}).sort('league_id'))
        return new_football_leagues

    @staticmethod
    def get_league_teams(league_id):
        """
        :return: list of teams playing a particular league.
        """
        stand_season = str(now.year)+'/'+str(now.year+1)
        teams = list(football_standings_conn.find({'league_id': league_id,'stand_season': stand_season},
                                                  projection = {'_id': False ,'games_won': False ,'team_points': False,
                                                                'stand_season': False, 'games_played': False,
                                                                'games_lost': False, 'games_drawn': False,
                                                                'position': False}).sort('team_name'))
        if not teams:
            stand_season = str(now.year-1)+'/'+str(now.year)
            teams = list(football_standings_conn.find({'league_id':league_id,'stand_season':stand_season},
                                                      projection = {'_id':False ,'games_won':False ,'team_points':False,
                                                                    'stand_season':False, 'games_played':False,
                                                                    'games_lost':False, 'games_drawn':False,
                                                                    'position':False}).sort('team_name'))
        return teams

    @staticmethod
    def get_team_squad(team_id):
        """
        returns: Team squad with manager name
        """
        return list(team_squad_conn.find({'team_id': int(team_id)}, projection={'_id': False}))

    @staticmethod
    def get_team_squads(team_1,team_2):
        """
        :return: full squad of two teams playing particular match.
        """
        team_1_squad = list(team_squad_conn.find({'team_id': int(team_1)}, projection={'_id': False}))
        team_2_squad = list(team_squad_conn.find({'team_id': int(team_2)}, projection={'_id': False}))
        squads = {'team_1_squad': team_1_squad,'team_2_squad': team_2_squad}
        return squads

    @staticmethod
    def get_player_stats(player_id):
        """
        :return: stats of particular player.
        """
        return list(player_profile_conn.find({'player_id':str(player_id) },projection={'_id': False}))

    @staticmethod
    def get_fixtures_new(date, league_id):
        """
        :return: fixtures of a league on specific 'date'.
        """
        return list(new_football_fixtures_conn.find({'league_id': int(league_id), 'match_date' : date}, projection = {'_id': False}))

    @staticmethod
    def get_league_specific_fixtures(league_id, fixture_type=None):
        """
        :return: fixtures for a league depending on the 'fixture_type'.
        """
        ep_now = calendar.timegm(time.gmtime())
        if fixture_type:
            if fixture_type == 'upcoming':
                league_fixtures = list(new_football_fixtures_conn.find({'league_id':league_id,'match_date_epoch':{'$gt':ep_now}},projection={'_id':False}).sort('match_date_epoch').limit(10))
            elif fixture_type == 'completed':
                league_fixtures = list(new_football_fixtures_conn.find({'league_id':league_id,'match_date_epoch':{'$lt':ep_now}},projection={'_id':False}).sort('match_date_epoch',-1).limit(10))
        else:
            league_fixtures = list(new_football_fixtures_conn.find({'league_id':league_id,'match_date_epoch':{'$lt':ep_now}},projection={'_id':False}).sort('match_date_epoch',-1).limit(10))
            league_fixtures_upcoming = list(new_football_fixtures_conn.find({'league_id':league_id,'match_date_epoch':{'$gt':ep_now}},projection={'_id':False}).sort('match_date_epoch').limit(10))
            league_fixtures.extend(league_fixtures_upcoming)
            league_fixtures.sort(key=operator.itemgetter('match_date_epoch'))
        return league_fixtures

    @staticmethod
    def get_team_upcoming_fixtures(team_id):
        """
        :return: upcoming fixtures of a team.
        """

        ep_now = calendar.timegm(time.gmtime())
        team_upcoming_fixtures = list(new_football_fixtures_conn.find({'home_team_id':int(team_id),'match_date_epoch':{'$gt':ep_now}},projection={'_id':False}).sort('match_date_epoch').limit(5))
        team_upcoming_fixtures_1 = list(new_football_fixtures_conn.find({'away_team_id':int(team_id),'match_date_epoch':{'$gt':ep_now}},projection={'_id':False}).sort('match_date_epoch').limit(5))
        team_upcoming_fixtures.extend(team_upcoming_fixtures_1)
        team_upcoming_fixtures.sort(key=operator.itemgetter('match_date_epoch'))
        return team_upcoming_fixtures

    @staticmethod
    def get_team_completed_fixtures(team_id):
        """
        :return: completed fixtures for a team.
        """
        ep_now = calendar.timegm(time.gmtime())
        team_completed_fixtures = list(new_football_fixtures_conn.find({'home_team_id':team_id,'match_status':'FT'},projection={'_id':False}).sort('match_date_epoch',-1).limit(5))
        team_completed_fixtures_1 = list(new_football_fixtures_conn.find({'away_team_id':team_id,'match_status':'FT'},projection={'_id':False}).sort('match_date_epoch',-1).limit(5))
        team_completed_fixtures_2 = list(new_football_fixtures_conn.find({'home_team_id':team_id,'match_status':'AET'},projection={'_id':False}).sort('match_date_epoch',-1).limit(5))
        team_completed_fixtures_3 = list(new_football_fixtures_conn.find({'away_team_id':team_id,'match_status':'AET'},projection={'_id':False}).sort('match_date_epoch',-1).limit(5))

        team_completed_fixtures.extend(team_completed_fixtures_1)
        team_completed_fixtures.extend(team_completed_fixtures_2)
        team_completed_fixtures.extend(team_completed_fixtures_3)
        team_completed_fixtures.sort(key=operator.itemgetter('match_date_epoch'), reverse = True)
        return team_completed_fixtures

    @staticmethod
    def get_match_scores(match_id):
        """
        :return: scores of a match.
        """
        return list(new_football_fixtures_conn.find({'match_id':int(match_id)},projection={'_id':False}))

    @staticmethod
    def get_todays_fixtures():
        """
        :return: all the fixtures from all the leagues on current day.
        """
        conn = project_utils.get_mongodb_connection()
        new_football_fixtures_conn = conn.football.new_football_fixtures
        todays_date = time.strftime('%d.%m.%Y', time.gmtime())
        return list(new_football_fixtures_conn.find({'match_date':todays_date},projection={'_id':False}).sort('match_date_epoch'))

    @staticmethod
    def get_league_standings(league_id):
        """
        :return: the league teams' standings.
        """
        return list(football_standings_conn.find({'league_id':str(league_id)},projection={'_id':False}).sort('position'))

    @staticmethod
    def get_team_form(team_1, team_2, league_id):
        """
        :return: last 5 performance records of 2 teams, in particular league.
        """
        teams_form = []
        try:
            print 'here'
            team_1_form = list(football_standings_conn.find({'team_id':int(team_1),'league_id':league_id},projection={'_id':False,'stand_group':False,'league_id':False,'league_name':False,'position':False,'season':False,'team_id':False,'sport_type':False}))
            team_2_form = list(football_standings_conn.find({'team_id':int(team_2),'league_id':league_id},projection={'_id':False,'stand_group':False,'league_id':False,'league_name':False,'position':False,'season':False,'team_id':False,'sport_type':False}))
            teams_form.extend(team_1_form)
            teams_form.extend(team_2_form)
            return teams_form
        except Exception as e:
            raise e

    @staticmethod
    def get_match_stats(match_id):
        """
        :return: statistics of a match.
        """
        stats = list(match_statistics_conn.find({'match_id': int(match_id)}, projection = {'_id': False}))
        return stats

    @staticmethod
    def get_match_teams(match_id):
        """
        :return: the players from both teams playing the match.
        """
        return list(match_teams_conn.find({'match_id': int(match_id)}, projection = {'_id': False}))

    @staticmethod
    def get_match_squads(match_id):
        """
        :return: the team,all substitutes,substitutions which happened and all the match events form the timeline of the match.
        """
        team = list(match_teams_conn.find({'match_id':int(match_id)},projection={'_id':False}))
        subs = list(match_substitutes_conn.find({'match_id':int(match_id)},projection={'_id':False}))
        substitutions = list(match_substitutions_all_conn.find({'match_id':int(match_id)},projection={'_id':False}))
        events = list(football_timeline_conn.find({'match_id':int(match_id)},projection={'_id':False}))
        if not team or not subs:
            match_squad = {}
        else:
            match_squad = {'teams': team, 'subs': subs, 'substitutions': substitutions, 'match_events': events}
        return match_squad

    @staticmethod
    def get_player_match_stats(match_id):
        """
        :return: game stats of the players playing the match.
        """
        return list(player_stats_conn.find({'match_id': int(match_id)}, projection = {'_id': False}))

    @staticmethod
    def get_match_substitutions(match_id):
        """
        :return: list of all substitutions happened over the course of the match.
        """
        return list(match_substitutions_all_conn.find({'match_id': int(match_id)}, projection = {'_id': False}))

    @staticmethod
    def get_match_subs(match_id):
        """
        :return: all the players from both teams who started the match on the bench i.e. can be substituted.
        """
        return list(match_substitutes_conn.find({'match_id':int(match_id)},projection = {'_id':False}))

    @staticmethod
    def get_match_summary(match_id):
        """
        :return: summary of the match which includes the cards and the goals scored by the players.
        """
        return list(match_summ_conn.find({'match_id' : int(match_id)}, projection = {'_id': False}))

    @staticmethod
    def get_match_timeline(match_id):
        """
        :return: timeline of the match which includes the yellow/red cards, substitutions and goals scored during the match.
        """
        return list(football_timeline_conn.find({'match_id': int(match_id)}, projection = {'_id':False}).sort('minute',-1))

    @staticmethod
    def get_upcoming_fixtures(max_limit=None):
        """
        :return: upcoming fixtures from all leagues.
        """
        date_today = time.strftime('%d.%m.%Y',time.gmtime())
        ep_tommorow = calendar.timegm(time.strptime(date_today,'%d.%m.%Y')) + 86400
        if max_limit:
            upcoming_fixtures = list(new_football_fixtures_conn.find({'match_date_epoch':{'$gt': ep_tommorow}},
                                                                     projection = {'_id':False}).sort('match_date_epoch',1).limit(max_limit))
        else:
            upcoming_fixtures = list(new_football_fixtures_conn.find({'match_date_epoch':{'$gt': ep_tommorow}},
                                                                     projection = {'_id':False}).sort('match_date_epoch', 1))
        return upcoming_fixtures


    @staticmethod
    def get_completed_fixtures():
        """
        :return: completed fixtures from all leagues.
        """
        ep_now = calendar.timegm(time.gmtime())
        completed_fixtures = list(new_football_fixtures_conn.find({'match_date_epoch':{'$lt': ep_now},'match_status': 'FT'}, projection = {'_id': False}).sort('match_date_epoch',-1).limit(6))
        completed_fixtures_1 = list(new_football_fixtures_conn.find({'match_date_epoch':{'$lt': ep_now},'match_status': 'AET'}, projection = {'_id': False}).sort('match_date_epoch',-1).limit(6))
        completed_fixtures.extend(completed_fixtures_1)
        completed_fixtures.sort(key=operator.itemgetter('match_date_epoch'), reverse= True)
        return completed_fixtures[:6]

    @staticmethod
    def get_commentary(match_id,comment_id=None,direction=None):
        """
        :return: commentary for the match.
        """
        if comment_id and direction == 'up':
            commentaries = list(football_comm_conn.find({'match_id': int(match_id),'id':{'$gt':comment_id}}, projection = {'_id': False}).sort('id').limit(20))
        elif comment_id and direction == 'down':
            commentaries = list(football_comm_conn.find({'match_id': int(match_id),'id':{'$lt':comment_id}}, projection = {'_id': False}).sort('id').limit(20))
        else:
            commentaries = list(football_comm_conn.find({'match_id': int(match_id)},projection={'_id':False}).sort('id'))
        return commentaries

    @staticmethod
    def get_squads(soup, team, league_id, team_id):
        """
        :return: players list for team squad.
        """
        player_list = []
        try:
            for s in soup.find_all('table', {'class':'tab-squad tab-squad-players'}):
                rows = s.find_all('tr')

            print team.upper()

            for row in rows:
                squad = row.find_all('td')
                if squad:
                    __dict = {'league_id': league_id ,'jersey': squad[1].string.strip(),'name': squad[2].text.strip(),
                              'nationality': squad[3].find('span').get('title').strip(), 'position': squad[4].string.strip(),
                              'age': squad[5].string.strip(), 'games': squad[6].string.strip(), 'goals': squad[7].string.strip(),
                              'assists': squad[8].string.strip(), 'yellow': squad[9].string.strip(),'red': squad[11].string.strip(),
                              'team_id': team_id}
                    player_list.append(__dict)

            manager = soup.find('table',{'class':'tab-squad tab-squad-manager'})
            return player_list,manager
        except Exception as e:
            raise e

    @staticmethod
    def get_player_profile(player_id):
        """
        :return: player profile from API
        """
        return player_profile_conn.find_one({'player_id':str(player_id)},projection = {'_id':False})

class GetFlagImage(BaseFlagImageHandler):
    """
    Returns flag image(s) of team(s).
    """
    @staticmethod
    def flag_single(team):
        return settings.FLAGS_IMAGE_URL.get(str(team), '')

    @staticmethod
    def flag_double(team_1, team_2):
        return [settings.FLAGS_IMAGE_URL.get(team_1, ''), settings.FLAGS_IMAGE_URL.get(team_2, '')]


class GetStadium(BaseStadiumHandler):
    """
    Returns stadium for a team.
    """
    @staticmethod
    def stadium(team_name):
        return settings.FOOTBALL_STADIUMS.get(str(team_name), '')
