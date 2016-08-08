#football_notifications.py

import os
import sys
import nltk
from termcolor import cprint
from pyfiglet import figlet_format
import requests
import json
from operator import itemgetter
from nltk.util import ngrams

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import sports.project.utils as project_utils
import settings


##converats a sentence into bigrams like [u'Match ends,', u'ends, Barcelona', u'Barcelona 1,', u'1, Valencia', u'Valencia 2.']
bigrams = lambda comment : [" ".join(_) for _ in ngrams(comment.split(), 2)]

class FootballNotifications:

    @staticmethod
    def check_event(match_id, new_comments):
        conn = project_utils.get_mongodb_connection()

        events = {'started': '3', 'goal': '7', 'penalty': '9'}
        bievents = {'red card': "4", "yellow card": "5", "full time": "6", "penalty missed": "11",  "own goal": "12", "second yellow": '4'}

        new_football_fixtures_conn = conn.football.new_football_fixtures
        league_id = new_football_fixtures_conn.find_one({'match_id': match_id}, projection = {'_id': False})['league_id']
        match_details  = new_football_fixtures_conn.find_one({'match_id': match_id}, projection= {'_id':False})
        match_score = str(match_details['home_team_score']) +'-'+ str(match_details['away_team_score']) +' '+ str(match_details['home_team']) +' vs '+ str(match_details['away_team'])
        

        for comment in new_comments:
            __comment = comment["comment"].lower()
            
            ##check if bievents keys are present into bigram tokenized sentence
            result = list(set.intersection(set(bievents.keys()), set(bigrams(__comment))))

            event_id = None
            if result:
                    event = result[0]
                    event_id = bievents[event]
            else:
                    try:
                        result = list(set.intersection(set(events.keys()), set(__comment.split())))
                        event_id = events[event]
                    except Exception:
                        pass

            top_text = comment["minute"] + comment["comment"]
            bottom_text = match_score
            if event_id:
                    FootballNotifications.notify(match_id, event_id, top_text, bottom_text, league_id)
        return

    @staticmethod
    def notify(match_id, event_id, tt, bt, league_id):
        """
        notification sample format : {'m' : '2183720', 'l' : '1399', 's' : '2', 'e' : '7', 'tt' : 'Leo Messi scores', 'bt' : 'Barcelon 1, Real Madrid 0', 'r' : 'l'}

        key description
        'm' = match_id of the match
        'l' = league_id of match
        's' = sport type (2 in case of football)
        'e' = event_id (unique to an event)
        'tt' = top text to show in the notification.
        'bt' = bottom text to show in the notification
        'r' = running status of match ('n' for not started ; 'l' for live ; 'f' for completed)
        """

        notification = {'m': match_id, 'l': league_id ,'s': 2, 'e': event_id ,'tt': tt, 'bt': bt, 'r': 'l'}
        response = requests.post(settings.NOTIFICATION_PRODUCTION_SERVER + settings.NOTIFICATION_ENDPOINT, data=json.dumps(notification))
        response_content = response.content
        print response.content
        conn = project_utils.get_mongodb_connection()
        sent_notifications = conn.football.sent_notifications
        sent_notifications.insert({'match_id': match_id, 'notification_content': notification, 'response': response_content})
        return
