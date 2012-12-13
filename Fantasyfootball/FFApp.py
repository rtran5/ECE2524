#!/usr/bin/python2
import urllib,urllib2,re,sys,os,time
from bs4 import BeautifulSoup
import ClientCookie
import ClientForm

class YahooFFLReader:
    def __init__(self,name,pw):
        self.name = name
        self.pw = pw
        self.base_url = 'http://football.fantasysports.yahoo.com'
        self.logged_in = False

    def login(self):
        # Sets the client webbrowser
        cookieJar = ClientCookie.CookieJar()
        opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cookieJar))
        opener.addheaders = [("User-agent","Mozilla/5.0 (compatible)")]
        ClientCookie.install_opener(opener)
        # Opens the login page for yahoo.com
        fp = ClientCookie.urlopen("http://login.yahoo.com")
        forms = ClientForm.ParseResponse(fp)
        fp.close()
        form = forms[0]
        form["login"] = self.name
        form["passwd"] = self.pw
        fp = ClientCookie.urlopen(form.click())
        fp.close()

    def get_info(self):
        # Opens the main page of the fantasy football
        fp = ClientCookie.urlopen(self.base_url)
        lines = fp.readlines()
        fp.close()
        text = "\n".join(lines)
        # Stores all of the lines in a temp.html file
        f = open('temp.html', 'w')
        f.write(text)
        f.close()
        # Use Beautiful Soup to parse the html.
        soup = BeautifulSoup(text)
        # Finds the teams on the page
        team_info = soup.find('div', {'class':'teams'})
        if team_info is None:       # Check login
            sys.stderr.write('Error: Login failed, parser limit exceeded or authentication failure, check username & password\n')
            sys.exit(1)
        # Stores the information about the users league
        userTeams = []
        userLeagueId = []
        for info in team_info.findAll('a', {'class':'team'}):
            userTeams.append(info.string)
            userLeagueId.append(info['href'])
        self.userTeams = userTeams
        self.userLeagueId = userLeagueId
  return (userTeams, userLeagueId)

    def retrieve_leagues(self, Choice):
        QuickFix = "?lhst=stand#lhststand"
        LeagueId = self.userLeagueId[Choice]
        LeagueSplit = LeagueId.split('/')
        LeagueSplit.pop()           # Truncated the end portion to get base link
        LeagueBase = "/".join(LeagueSplit)
        
        #----> Option to pick the league you want to open <------#
        fp = ClientCookie.urlopen(self.base_url + LeagueBase + QuickFix)
        lines = fp.readlines()
        fp.close()
        text = "\n".join(lines)
        # Use Beautiful Soup to parse the html
        soup = BeautifulSoup(text)
        # Finds the teams on the page
        team_info = soup.find('table',{'class' : 'gametable'})
        teams = {}
        # Gets the information on the teams in the league 
        str_list = []
        LeagueTeamIds = []
        for info in team_info.findAll('tr', {'class':{'odd','even'}}):
            temp_list = []
            for eachTeam in info.findAll('td'):
                temp_list.append(eachTeam.string)
                for moreInfo in eachTeam.findAll('a'):
                    LeagueTeamIds.append(moreInfo['href'])
            str_list.append(' '.join(temp_list))
        self.LeagueTeamIds = LeagueTeamIds
        return LeagueTeamIds, str_list

    def display_players(self, Choice):
        Id = self.LeagueTeamIds[Choice]
        
        fp = ClientCookie.urlopen(self.base_url + Id)
        lines = fp.readlines()
        fp.close()
        text = "\n".join(lines)
        # Use Beautiful Soup to parse the html
        soup = BeautifulSoup(text)
        # Finds the players on the page
        team_info = soup.find('table', {'class' : 'teamtable'})
        teams = {}
        # Gets the information on the teams in the league 
        playerNames = []
        playerPos = []
        conditions = []
        stats = []
        temp_list = []
        
        # Find the specific html portion with the players' names
        for info in team_info.findAll('a', {'class' : 'name'}):
            playerNames.append(info.string)
        # Find the specific html portion with the players' positions
        for info in team_info.findAll('td', {'class' : 'pos first'}):
            playerPos.append(info.string)
        # Find the specific html portion with the team positions
        for info in team_info.findAll('span'):
            if info.string != None and info.string.find("(") != -1:
                conditions.append(info.string)
        i = 1
        # Find the specific html portion with the players' stats
        for info in team_info.findAll('td', {'class' : 'stat'}):
            temp_list.append(info.string)
            if i % 11 == 0:
                stats.append(' '.join(temp_list))
                temp_list = []
            i = i + 1

        return (playerNames, playerPos, conditions, stats)
