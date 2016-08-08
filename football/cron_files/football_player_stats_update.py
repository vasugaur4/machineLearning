#!/usr/bin/env python
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import sports.project.utils as project_utils
from sports.football.add_data import AddFootballData


if __name__ == '__main__':
    conn = project_utils.get_mongodb_connection()
    team_squad_conn = conn.football.team_squad
    teams = list(team_squad_conn.find(projection= {'_id':False}))
    for team in teams:
        for player in team['players']:
            try:
                print player['name'],player['id']
                AddFootballData.update_player_stats(player['id'])
            except Exception as e:
                print e
            time.sleep(2)
