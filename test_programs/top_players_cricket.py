#!usr/bin/env python


import requests
from bs4 import BeautifulSoup
import pymongo

class TopCricketPlayers:

    def __init__(self,link):

        self.link = link
        response = requests.get(self.link)
        self.soup = BeautifulSoup(response.content)
        conn = pymongo.MongoClient()
        db = conn.cricket
        self.top_cricket_players = db.top_cricket_players


    def get_players(self):

        table = self.soup.findAll('table',{'class':'cricket-allRecordsTable'})

        for player in table[1].findAll('tr'):
            try:

                link = player.findAll('a')[1].get('href')
                res = requests.get('http://www.thatscricket.com/'+link)
                soup = BeautifulSoup(res.content)
                #description = soup.find('div',{'class':'cricket-profileDesc'})
                full_name=soup.find('div',{'class':'cricket-profileText'})
                self.top_cricket_players.insert({'name':full_name.text})
                print full_name.text

            except Exception,e:
                pass
        
def main():
    #obj = TopCricketPlayers('http://www.espncricinfo.com/ci/content/rss/feeds_rss_cricket.html')
    obj = TopCricketPlayers('http://www.thatscricket.com/statistics/')
    obj.get_players()


if __name__ == '__main__':main()


            
