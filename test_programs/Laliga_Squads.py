#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from itertools import izip
class Squads:
	def __init__(self,link,team):
			res = requests.get(link)
			self.soup = BeautifulSoup(res.content)
			self.team = team
			
	def get_squads(self):
			for s in self.soup.find_all('table',{'class':'tab-squad tab-squad-players'}):
				rows=s.find_all('tr')
			
			print self.team.upper()
			print 
			for row in rows:
					squad=row.find_all('td')
					try:
						print 'Jersey:',squad[1].string.strip(),'Name:',squad[2].text.strip(),'Nationality:',squad[3].find('span').get('title').strip(),'Position:',squad[4].string.strip()
						print 'Age:',squad[5].string.strip(),'Games:',squad[6].string.strip(),'Goals:',squad[7].string.strip(),'Assists:',squad[8].string.strip(),'Yellow:',squad[9].string.strip(),'Red:',squad[11].string.strip()
					except Exception as e:
						print e

if __name__=='__main__':
	list_of_teams = ['athletic-club','atletico-madrid','barcelona','celta-de-vigo','deportivo-la-coruna',
	'eibar','espanyol','getafe','granada','las-palmas',
	'levante','malaga','rayo-vallecano','real-betis','real-madrid',
	'real-sociedad','sevilla','sporting-gijon','valencia','villarreal']

	list_of_ids = ['/2019?ICID=SP_TN_109','/2020?ICID=SP_TN_110','/2017?ICID=TP_TN_111','/2033?ICID=TP_TN_112',\
			'/2018?ICID=TP_TN_113','/2042?ICID=TP_TN_114','/2032?ICID=TP_TN_115','/2039?ICID=TP_TN_116','/7072?ICID=TP_TN_117',\
			'/2055?ICID=TP_TN_118','/2036?ICID=TP_TN_119','/2024?ICID=TP_TN_120','/2054?ICID=TP_TN_121','/2025?ICID=TP_TN_122',\
			'/2016?ICID=TP_TN_123','/2028?ICID=TP_TN_124','/2021?ICID=TP_TN_125','/2038?ICID=TP_TN_126','/2015?ICID=TP_TN_127',\
			'/2023?ICID=TP_TN_128']

	for team,_id in izip(list_of_teams,list_of_ids):
		url = 'http://www.goal.com/en-us/teams/spain/primera-division/7/'+team+_id
		obj = Squads(url,team)
		obj.get_squads()
