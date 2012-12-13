#!/usr/bin/python2
import urllib,urllib2,re,sys,os,time
from bs4 import BeautifulSoup
import ClientCookie
import ClientForm
import logging
FORMAT = '%(levelname)s %(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class YahooFFLReader:
    def __init__(self,name,pw):
        self.name = name
        self.base_url = 'http://football.fantasysports.yahoo.com/'
	self.base_league_url = "http://football.fantasysports.yahoo.com/f1/"
        self.pw = pw
        self.logged_in = False

    def login(self):
        logger.info('Logging in')
        if not self.logged_in:
            return
        cookieJar = ClientCookie.CookieJar()
        opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cookieJar))
        opener.addheaders = [("User-agent","Mozilla/5.0 (compatible)")]
        ClientCookie.install_opener(opener)
        fp = ClientCookie.urlopen("http://login.yahoo.com")
        forms = ClientForm.ParseResponse(fp)
        fp.close()
        form = forms[0]
        form["login"] = self.name
        form["passwd"] = self.pw
        fp = ClientCookie.urlopen(form.click())
        fp.close()

    def retrieve_leagues(self):
        logger.info('Retrieving leagues')
	#Sets the client webbrowser
        cookieJar = ClientCookie.CookieJar()
        opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cookieJar))
        opener.addheaders = [("User-agent","Mozilla/5.0 (compatible)")]
        ClientCookie.install_opener(opener)
	#Opens the login page for yahoo.com
        fp = ClientCookie.urlopen("http://login.yahoo.com")
        forms = ClientForm.ParseResponse(fp)
        fp.close()
        form = forms[0]
        form["login"] = self.name
        form["passwd"] = self.pw
        fp = ClientCookie.urlopen(form.click())
        fp.close()
	#Opens the main page of the fantasy football
        fp = ClientCookie.urlopen(self.base_url)
        lines = fp.readlines()
        fp.close()
        text = "\n".join(lines)
	#Stores all of the lines in a temp.html file
        f = open('temp.html', 'w')
        f.write(text)
        f.close()
	#Use Beautiful Soup to parse the html.
        soup = BeautifulSoup(text)
	#Finds the teams on the page
        team_info = soup.find('div', {'class':'teams'})
        teams = {}
	#Stores the information about the users league
        for info in team_info.findAll('a', {'class':'team'}):
            teams[info.string] = {'url' : info['href'],'league' : info['href']}
        logger.info('Teams: ' + str(teams))
        self.teams = teams
	#----> Option to pick the league you want to open <------#
	fp = ClientCookie.urlopen("http://football.fantasysports.yahoo.com/f1/658285")
        lines = fp.readlines()
        fp.close()
        text = "\n".join(lines)
	#Use Beautiful Soup to parse the html
        soup = BeautifulSoup(text)
	#Finds the teams on the page
        team_info = soup.find('table',{'class' : 'gametable'})
        teams = {}
	#Gets the information on the teams in the league 
	str_list = []
 	for info in team_info.findAll('tr', {'class':'even'}):
	    temp_list = []
            for eachTeam in info.findAll('td'):
		temp_list.append(eachTeam.string)
	    str_list.append(' '.join(temp_list))
	for info in team_info.findAll('tr', {'class':'odd'}):
	    temp_list = []
            for eachTeam in info.findAll('td'):
		temp_list.append(eachTeam.string)
	    str_list.append(' '.join(temp_list))
	print '\n'.join(str_list)

    def to_num(self,str):
        str = str.replace(',','')
        return float(str)

def main(name,pw):
    #num_pages = 10
    reader = YahooFFLReader(name,pw)
    print "Logged"
    reader.retrieve_leagues()
    #time.sleep(5)
    #reader.retrieve_player_stats('192418',num_pages)
    #reader.write_stats()

if __name__ == "__main__":
    name = sys.argv[1]
    pw = sys.argv[2]
    main(name,pw)
