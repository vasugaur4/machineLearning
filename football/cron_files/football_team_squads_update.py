#!/usr/bin/env python
import os
import requests
import sys
import time
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from sports.football import utils
import settings
import sports.project.utils as project_utils
from sports.football.fetch_data import FootBallData
from sports.football.add_data import AddFootballData


if __name__=='__main__':
    print 'cron running to update team squads'
    conn = project_utils.get_mongodb_connection()
    football_standings_conn = conn.football.football_standings
    for team in football_standings_conn.find(projection={'_id':False}).sort('team_id'):
        try:
            AddFootballData.add_team_squads(team['team_id'])
            time.sleep(1)
        except Exception as e:
            print e