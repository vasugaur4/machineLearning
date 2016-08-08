#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

class Squads:
		
	def __init__(self,link,team):
			res = requests.get(link)
			self.soup = BeautifulSoup(res.content,'html.parser')
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
	list_of_teams = ['afc-bournemouth','arsenal','aston-villa','chelsea','crystal-palace',
	'everton','leicester-city','liverpool','manchester-city','manchester-united',
	'norwich-city','southampton','stoke-city','sunderland','swansea-city',
	'tottenham-hotspur','watford','west-bromwich-albion','west-ham-united']
	
	list_of_ids = ['/711?ICID=SP_TN_91','/660?ICID=TP_TN_92','/665?ICID=TP_TN_93','/661?ICID=TP_TN_94','/679?ICID=TP_TN_95',
	'/674?ICID=TP_TN_96','/682?ICID=TP_TN_97','/663?ICID=TP_TN_98','/676?ICID=TP_TN_99','/662?ICID=TP_TN_100',
	'/677?ICID=TP_TN_102','/670?ICID=TP_TN_103','/690?ICID=TP_TN_104','/683?ICID=TP_TN_105','/738?ICID=TP_TN_106',
	'/675?ICID=TP_TN_107','/696?ICID=TP_TN_108','/678?ICID=TP_TN_109','/684?ICID=TP_TN_110']

	for team,_id in zip(list_of_teams,list_of_ids):
		url = 'http://www.goal.com/en-us/teams/england/premier-league/8/'+team+_id
		obj = Squads(url,team)
		obj.get_squads()
