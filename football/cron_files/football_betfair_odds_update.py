#!/usr/bin/env python
import datetime
import json
import os
import pprint
import pymongo
import requests
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import settings
import sports.project.utils as project_utils

class BetfairOdds:

    def __init__(self):
        self.endpoint = settings.AUS_BETFAIR_URL
        self.endpoint_uk = settings.UK_BETFAIR_URL
        header = {'X-Application': 'Y0yB2Zob0L0dSONJ', 'X-Authentication': settings.BETFAIR_AUTHENTICATION_KEY, 'Accept': 'application/json'}
        res = requests.post(settings.BETFAIR_KEEP_ALIVE_URL, headers=header)
        keep_alive_token = json.loads(res.content)['token']
        self.headers = {'X-Application': 'Y0yB2Zob0L0dSONJ', 'X-Authentication': keep_alive_token, 'content-type': 'application/json'}
        self.list_of_competitions = []
        self.list_of_market = []
        self.temp_dict = {}

    def get_marketID(self):
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        json_req = '{"filter":{ "eventTypeIds":["1"] }, "max_results":"30"}'
        url = self.endpoint_uk + "listEvents/"
        response = requests.post(url, data=json_req, headers=self.headers)
        self.list_of_competitions = json.loads(response.content)

        for competition in self.list_of_competitions:
            eventId = competition['event']['id']
            market_catalouge_req = '{"filter":{"eventIds":["' + eventId + '"],"marketTypeCodes":["MATCH_ODDS"],"marketBettingTypes":["ODDS"],"marketStartTime":{"from":"' + now + '"}},"sort":"FIRST_TO_START",\
            "maxResults":"100","marketProjection":["RUNNER_METADATA","RUNNER_DESCRIPTION","COMPETITION","MARKET_START_TIME"]}'
            url = self.endpoint_uk + "listMarketCatalogue/"
            response = requests.post(url, data=market_catalouge_req, headers=self.headers)
            if json.loads(response.content):
                self.list_of_market.append(json.loads(response.content)[0])
            else:
                print competition
        pprint.pprint(self.list_of_market)

        res = requests.get(settings.FOOTBALL_GET_ALL_MATCHES_URL)
        list_of_recent_football_matches = json.loads(res.content)
        for x in self.list_of_market:
            runners = x['runners']
            runnerNameList = [runners[0]['runnerName'], runners[1]['runnerName']]
            for match in list_of_recent_football_matches['data']['football']:
                if {match['away_team'], match['home_team']}.issubset(runnerNameList):
                    for runner in runners:
                        self.get_book(x['competition']['id'], x['competition']['name'], x['marketId'], runner['runnerName'], runner['selectionId'])

    def update_dict(self, res, selectionId, marketId, competitionName, runnerName):
        marketBook = res
        try:
            runners = marketBook[0]['runners']
            for runner in runners:
                if runner['selectionId'] == selectionId:
                    print 'Odds of '+ str(runnerName) +' winning : ' + str(runner['ex']['availableToBack'][1]['price'])
                    self.temp_dict.setdefault(marketId,{}).setdefault(competitionName,[]).append({runnerName:str(runner['ex']['availableToBack'][1]['price'])})
                else:
                    print 'didn\'t match'
        except Exception as e:
            print e

    def get_book(self, competitionId, competitionName, marketId, runnerName, selectionId):
        market_book_req = '{"marketIds":["' + marketId + '"],"priceProjection":{"priceData":["EX_BEST_OFFERS"]}}'
        url = self.endpoint + "listMarketBook/"
        response = requests.post(url, data=market_book_req, headers=self.headers)
        res = json.loads(response.content)
        if res:
            self.update_dict(res, selectionId, marketId, competitionName, runnerName)
        else:
            url = self.endpoint_uk + "listMarketBook/"
            response = requests.post(url, data=market_book_req, headers=self.headers)
            res = json.loads(response.content)
            self.update_dict(res, selectionId, marketId, competitionName, runnerName)

        pprint.pprint(self.temp_dict)

        conn = project_utils.get_mongodb_connection()
        db = conn.betfair_odds
        football_odds = db.football_odds
        for odds in self.temp_dict:
            try:
                values = self.temp_dict[odds].values()[0]
                t1 = values[0]
                t2 = values[1]
                t3 = values[2]
                football_odds.update({'team_1':str(t1.keys()[0]),'team_2':str(t2.keys()[0])},
                                     {'$set': {'marketId':odds,
                                               'team_1': str(t1.keys()[0]),
                                               'team_2': str(t2.keys()[0]),
                                               'team_1_odds': t1.values()[0],
                                               'team_2_odds': t2.values()[0],
                                               'draw_odds': t3.values()[0]}},upsert=True)
            except Exception as e:
                print e


if __name__ == "__main__":
    obj = BetfairOdds().get_marketID()
