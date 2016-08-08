#!/usr/bin/env python
import os
import sys
import calendar
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
import sports.project.utils as project_utils
from sports.football.add_data import AddFootballData


if __name__ == '__main__':
    print 'cronjob running for football upcoming fixtures update'
    date = time.strftime('%d.%m.%Y',time.gmtime())
    print date
    ep_date = calendar.timegm(time.strptime(date,'%d.%m.%Y'))
    for x in xrange(7):
        new_date = time.strftime('%d.%m.%Y',time.gmtime(ep_date - 86400))
        print new_date
        AddFootballData.upcoming_fixtures(new_date)
        ep_date += 86400
