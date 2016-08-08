#!/usr/bin/env python

import requests
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import sports.project.utils as project_utils
import settings

class RegisterMatches:

    def __init__(self,url):

        self.register_matches = {}
        response = requests.get(url)
        self.data = json.loads(response.content)

    def get_matches(self):

        for match in self.data['data']:
            self.register_matches.setdefault('matches',list()).append({'name':match['home_team']+' vs '+ match['away_team'],'id':str(match['match_id'])+'|'+str(match['league_id'])})

        self.post_matches(self.register_matches)

    def post_matches(self,register_matches):

        print register_matches
        url = settings.REGISTER_MATCH_SERVER_IP_2 + settings.REGISTER_MATCH_URL
        res = requests.post(url,data=json.dumps(register_matches))
        print res.content


if __name__ == '__main__':
    server_url = settings.APPLICATION_SERVER_IP + settings.FOOTBALL_UPCOMING_FIXTURES_ENDPOINT
    obj = RegisterMatches(server_url)
    obj.get_matches()
