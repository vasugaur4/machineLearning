import calendar
import os
import pymongo
import sys
import nltk
import time
from football_notifications_test import FootballNotifications

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import sports.project.utils as project_utils


def get_match_data(match_commentaries):
    """
    :rtype: object
    """
    try:
        match_stats = match_commentaries.get('match_stats', {})
        match_subs = match_commentaries.get('subs', {})
        match_player_stats = match_commentaries.get('player_stats', {})
        single_match_teams = match_commentaries.get('lineup', {})
        match_substitutions = match_commentaries.get('substitutions', {})
        return (match_stats, match_subs, match_player_stats, single_match_teams, match_substitutions)
    except Exception as e:
        print 'error in get match data'


def add_match_commentary(match_id, commentaries_comments):
        new_comments = list()
        conn = project_utils.get_mongodb_connection()
        football_comm = conn.football.football_comm
        FootballNotifications.test(match_id, commentaries_comments)
        try:
                for comment in commentaries_comments:
                        if 'bet365' in nltk.word_tokenize(comment['comment']):
                                pass
                        else:
                                try:
                                        data = {'match_id': match_id, 'comment': comment['comment'],
                                              'id': int(comment['id']),
                                              'minute': comment['minute'],
                                              "time": time.time()}

                                        football_comm.insert(data)
                                        new_comments.append(data)
                                except pymongo.errors.DuplicateKeyError:
                                        pass
                                        
    except Exception as e:
        print 'error in add_match_commentary',commentaries_comments
    return new_comments


def add_match_subs(match_id, match_subs):
    conn = project_utils.get_mongodb_connection()
    match_substitutes = conn.football.match_substitutes
    try:
        for team in match_subs:
            for subs in match_subs[team]:
                match_substitutes.update({'match_id': match_id,'player_name': subs['name']},
                                         {'$set':{'match_id': match_id,
                                                  'team':team,
                                                  'player_name':subs['name'],
                                                  'jersey_number': subs['number'],
                                                  'position': subs['pos'],
                                                  'player_id':subs['id']}},upsert = True)
    except Exception as e:
        print 'error in add_match_subs',match_subs
    return


def add_match_stats(match_id, match_stats):
    conn = project_utils.get_mongodb_connection()
    match_statistics = conn.football.match_statistics
    try:
        for team in match_stats:
            for stats in match_stats[team]:
                match_statistics.update({'match_id' : match_id, 'team' : team},
                                        {'$set':{'match_id':match_id,
                                                 'team':team,
                                                 'shots_ongoal':stats['shots_ongoal'],
                                                 'fouls':stats['fouls'],
                                                 'corners':stats['corners'],
                                                 'saves':stats['saves'],
                                                 'offsides':stats['offsides'],
                                                 'possesiontime':stats['possesiontime'].split('%')[0],
                                                 'redcards':stats['redcards'],
                                                 'yellowcards':stats['yellowcards'],
                                                 'shots_total':stats['shots_total']}},upsert = True)
    except Exception as e:
        print 'error in add_match_stats',match_stats
    return


def add_match_summary(match_id, match_events):
    conn = project_utils.get_mongodb_connection()
    match_summ = conn.football.match_summ
    try:
        for event in match_events:
            match_summ.update({'event_time':event['minute'],'match_id':match_id,'event':event['type'],'player_name':event['player']},
                              {'$set':{'match_id':match_id,
                                       'event_time':event['minute'],
                                       'event':event['type'],
                                       'team':event['team'],
                                       'player_name':event['player'],
                                       'assist':event['assist'],
                                       'extra_min':event['extra_min'],
                                       'player_id':event['player_id'],}},upsert=True)
    except Exception as e:
        print 'error in add_match_summary',match_events
    return


def add_players_stats(match_id, match_player_stats):
    conn = project_utils.get_mongodb_connection()
    player_stats = conn.football.player_stats
    try:
        for team in match_player_stats:
            for all_players in match_player_stats[team]:
                for player in match_player_stats[team][all_players]:
                    player_stats.update({'match_id': match_id, 'name': player['name']},
                                        {'$set':{'match_id':match_id,
                                                 'name': player['name'],
                                                 'team': team,
                                                 'offsides': player['offsides'],
                                                 'pen_scored': player['pen_score'],
                                                 'pen_missed': player['pen_miss'],
                                                 'fouls_commited': player['fouls_committed'],
                                                 'saves': player['saves'],
                                                 'position': player['pos'],
                                                 'redcards': player['redcards'],
                                                 'fouls_drawn': player['fouls_drawn'],
                                                 'assists': player['assists'],
                                                 'yellowcards': player['yellowcards'],
                                                 'shots_total': player['shots_total'],
                                                 'shots_on_goal': player['shots_on_goal'],
                                                 'jersey_number': player['num'],
                                                 'goals': player['goals'],
                                                 'player_id': player['id']}},upsert = True)
    except Exception as e:
        print 'print error in add_match_stats',match_player_stats
    return


def add_match_teams(match_id, single_match_teams):
    conn = project_utils.get_mongodb_connection()
    match_teams = conn.football.match_teams
    try:
        for team in single_match_teams:
            for player in single_match_teams[team]:
                match_teams.update({'match_id':match_id, 'name':player['name']},
                                   {'$set':{'match_id':match_id,
                                            'team':team,
                                            'name':player['name'],
                                            'position': player['pos'],
                                            'jersey_number': player['number'],
                                            'player_id':player['id']}},upsert = True)
    except Exception as e:
        print 'error in add_match_teams',single_match_teams
    return


def add_match_substitutions(match_id, match_substitution):
    conn = project_utils.get_mongodb_connection()
    match_substitutions_all = conn.football.match_substitutions_all
    try:
        for team in match_substitution:
            for player in match_substitution[team]:
                match_substitutions_all.update({'match_id': match_id, 'player_on':player['on_name'], 'player_off': player['off_name']},
                                               {'$set':{'match_id': match_id,
                                                        'team': team,
                                                        'minute': player['minute'],
                                                        'player_off': player['off_name'],
                                                        'player_off_id': player['off_id'],
                                                        'player_on': player['on_name'],
                                                        'player_on_id': player['on_id']}},upsert = True)
    except Exception as e:
        print 'error in add_match_substitutions',match_substitution
    return


def add_match_timeline(match_id, match_substitution, match_events):
    conn = project_utils.get_mongodb_connection()
    football_timeline = conn.football.football_timeline
    try:
        for team in match_substitution:
            for player in match_substitution[team]:
                football_timeline.update({'match_id': match_id, 'player_on': player['on_name'], 'player_off': player['off_name']},
                                         {'$set': {'match_id': match_id,
                                                   'team': team,
                                                   'minute': player['minute'],
                                                   'player_off': player['off_name'],
                                                   'player_off_id': player['off_id'],
                                                   'player_on': player['on_name'],
                                                   'player_on_id': player['on_id']}}, upsert=True)

        for event in match_events:
            football_timeline.update({'event_time': event['minute'], 'match_id': match_id, 'event': event['type'],
                               'player_name': event['player']},
                              {'$set': {'match_id': match_id,
                                        'event_time': event['minute'],
                                        'event': event['type'],
                                        'team': event['team'],
                                        'player_name': event['player'],
                                        'assist': event['assist'],
                                        'extra_min': event['extra_min'],
                                        'player_id': event['player_id'],}}, upsert=True)
    except Exception as e:
        print 'error in add_match_timeline'
    return
