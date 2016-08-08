import sys
import os
import pymongo

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import sports.project.utils as project_utils
from sports.football.add_data import AddFootballData


def update_standings():
    conn = project_utils.get_mongodb_connection()
    new_football_leagues_conn = conn.football.new_football_leagues
    for x in new_football_leagues_conn.find().sort('league_id'):
        AddFootballData.add_league_standings(x['league_id'])
        print x['league_id']


if __name__ == '__main__':
    print 'cronjob working for football standings update'
    update_standings()
