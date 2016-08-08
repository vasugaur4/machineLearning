#football_notifications.py

import os
import sys
import nltk
from termcolor import cprint
from pyfiglet import figlet_format
import requests
import json
from operator import itemgetter

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import sports.project.utils as project_utils
import settings

class FootballNotifications:

    @staticmethod
    def check_event(match_id, new_comments):
        conn = project_utils.get_mongodb_connection()

        events = {'Started':'3', 'Red Card':'4', 'Yellow Card':'5','Full time':'6', 'Goal':'7','Penalty':'9', 'Penalty missed':'11', 'Own Goal':'12'}

        new_football_fixtures_conn = conn.football.new_football_fixtures
        league_id = new_football_fixtures_conn.find_one({'match_id':match_id}, projection = {'_id':False})['league_id']
        match_details  = new_football_fixtures_conn.find_one({'match_id':match_id}, projection= {'_id':False})
        match_score = str(match_details['home_team_score']) +'-'+ str(match_details['away_team_score']) +' '+ str(match_details['home_team']) +' vs '+ str(match_details['away_team'])

        for comment in new_comments:
            try:
                tokenized_sent = comment['comment'].split()

                if 'Own' in tokenized_sent and 'Goal' in tokenized_sent:
                    # cprint(figlet_format('Own Goal', font='starwars'), attrs=['bold'])
                    # print comment['comment']
                    # event_id = events.get('Own Goal')
                    # top_text = comment['minute']+' '+
                    pass

                elif 'Goal' in tokenized_sent and 'Own' not in tokenized_sent:
                    cprint(figlet_format('Goal', font='starwars'), attrs=['bold'])
                    print comment['comment']
                    event_id = events.get('Goal')
                    top_text = comment['minute'] +' '+ nltk.sent_tokenize(comment['comment'])[2].split(' (')[0]+' scores!'
                    bottom_text = nltk.sent_tokenize(comment['comment'])[1]
                    FootballNotifications.notify(match_id, event_id, top_text, bottom_text, league_id)
                    print '*' * 20

                elif 'yellow' in tokenized_sent:
                    cprint(figlet_format('Yellow card', font='starwars'), attrs=['bold'])
                    print comment['comment']
                    if comment['comment'].split(' card')[0] == 'Second yellow':
                        event_id = events.get('Red Card')
                        top_text = comment['minute'] + comment['comment'].split(')')[0]+')'
                        bottom_text = match_score
                        FootballNotifications.notify(match_id, event_id, top_text, bottom_text, league_id)
                    else:
                        event_id = events.get('Yellow Card')
                        top_text = comment['minute'] +' '+ comment['comment'].split('card')[0]+'card'
                        bottom_text = match_score
                        FootballNotifications.notify(match_id, event_id, top_text, bottom_text, league_id)
                    print '*' * 20

                elif 'red' in tokenized_sent:
                    cprint(figlet_format('Red card', font='starwars'), attrs=['bold'])
                    print comment['comment']
                    event_id = events.get('Red Card')
                    top_text = comment['minute'] +' '+ comment['comment'].split('card')[0]+'card'
                    bottom_text = match_score
                    FootballNotifications.notify(match_id, event_id, top_text, bottom_text, league_id)
                    print '*' * 20

                elif 'Penalty' in tokenized_sent and 'conceded' in tokenized_sent:
                    cprint(figlet_format('Penalty conceded', font='starwars'), attrs=['bold'])
                    print comment['comment']
                    event_id = events.get('Penalty')
                    top_text = comment['minute'] +' '+ comment['comment'].split(')')[0]+')'
                    bottom_text = match_score
                    FootballNotifications.notify(match_id, event_id, top_text, bottom_text, league_id)

                elif 'Penalty' in tokenized_sent and 'missed' in tokenized_sent:
                    cprint(figlet_format('Penalty missed!', font='starwars'), attrs=['bold'])
                    print comment['comment']
                    event_id = events.get('Penalty missed')
                    top_text = comment['minute'] +' '+ comment['comment'].split(')')[0]+')'
                    bottom_text = match_score
                    FootballNotifications.notify(match_id, event_id, top_text, bottom_text, league_id)
            except Exception as e:
                print e
        return

    @staticmethod
    def notify(match_id, event_id, tt, bt, league_id):
        notification = {'m': match_id, 'l': league_id ,'s': 2, 'e': event_id ,'tt': tt, 'bt': bt, 'r': 'l'}
        response = requests.post(settings.NOTIFICATION_PRODUCTION_SERVER + settings.NOTIFICATION_ENDPOINT, data=json.dumps(notification))
        response_content = response.content
        print response.content
        conn = project_utils.get_mongodb_connection()
        sent_notifications = conn.football.sent_notifications
        sent_notifications.insert({'match_id': match_id, 'notification_content': notification, 'response': response_content})
        return
