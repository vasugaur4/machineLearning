#!/usr/bin/env python
import sys
import os
import time
import pymongo

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import sports.project.utils as project_utils
from sports.football.add_data import AddFootballData


if __name__ == '__main__':
    print 'Running cron job to update Football live scores'
    print time.strftime("%d/%m/%Y"),time.strftime("%H:%M:%S")
    try:
        AddFootballData.todays_fixtures()
    except Exception as e:
        print e
