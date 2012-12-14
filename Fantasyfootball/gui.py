#!/usr/bin/python2
import FFClass
import re
import sys

def mainMenu():

#displays the main menu for the user to navigate.
	indent()
	print "Main Menu Options"
	print ""
	print "     1) Log in"
	print "     2) Exit"
	print ""
	choice = raw_input("Enter your choice: ")
	if(choice == "1"):
		print "Log in selected" 
		logIn()
	elif(choice == "2"):
		print "Exiting the program"
		sys.exit(0)
	else: 
		print "Invalid choice"
		mainMenu()

def logIn():

#receives information from the user so the user can access his league.  Ask's his league username and password, then access's that leagues data from Yahoo.
	indent()
	username = raw_input("Please enter a username: ")
	password = raw_input("please enter a password: ")

	reader = FFClass.YahooFFLReader(username, password)
   	print "Logging into " + username
	reader.login()
	teamNames, teamID = reader.get_info()
	teamMenu(username, reader, teamNames, teamID)

#	teamMenu(username, reader)
#	reader.retrieve_leagues()

def teamMenu(username, reader,teamNames, teamID):

#displaying the two leagues available.  Ask's the user for a choice to view more in depth information on the league. The user can also exit the program.
	x = 1
	indent()
	print "Display " +username + " Teams Menu"
	print ""
	for teams in teamNames:
		print str(x) +") "+ teams
		x = x+1
	print str(x)+") Exit"
	print ""
	choice = raw_input("Enter your choice: ")

	if(int(choice) <= len(teamNames)):
		if(int(choice) > 0):
			data, strList = reader.retrieve_leagues(int(choice)-1)
			displayStats(username,reader, data, strList)
		else:
			print "Invalid argument" 
			teamMenu(username, reader,teamNames)
	elif(int(choice) == (len(teamNames)+1)):
		print "Exiting the program"
		sys.exit(0)
	else:
		print "Invalid argument"
		teamMenu(username, reader,teamNames, teamID)

def displayStats(username,reader, data, strList):

#displaying the stats and names of the teams.  Ask's the user for a choice input to view more in depth information on that team selected
	indent()
	print "Displaying all the teams and wins rations"
	print ""
	print "Ranking  Name  Win/Loss  % winning  Points Scored  Points Scored Against  Streak  Waiver#  Moves"
	print ""
	x = 1
	for teams in strList:
		print str(x) +") "+ teams
		x = x+1
		y = x+1
	print str(x)+") Exit"
	print str(y) + ") Previous Menu"
	print ""
	choice = raw_input("Enter your choice to see teams players/stats: ")

#option for user to select which team to view
	if(int(choice) <= len(data)):
		if(int(choice) > 0):
			(playerNames, playerPos, playerCond, playerStat) = reader.display_players(int(choice)-1)
			displayPlayers(reader, playerNames, playerPos, playerCond, playerStat, data, username, strList)
		else:
			print "Invalid argument" 
			displayStats(username,reader, data, strList)

#option to go back to team menu
	elif (int(choice) == (len(data)+2)):
		(teamNames, teamID) = reader.get_info()
		teamMenu(username, reader, teamNames, teamID)

#option if the user wants to quit the program
	elif(int(choice) == (len(data)+1)):
		print "Exiting the program"
		sys.exit(0)
	else:
		print "Invalid argument"
		displayStats(username,reader, data, strList)

def displayPlayers(reader, playerNames, playerPos, playerCond, playerStat, data, username, strList):  
#displays the players from the selected team.  Show's players names, positions, conditions, stats, or everything if the user wishes to view that.6
	i = 0
	print "Category Menu"
	print ""
	print "1: Positions"
	print "2: Positions on team"
	print "3: Stats"
	print "4: Exit"
	print "5: Previous Menu"
	print ""
	choice = raw_input("Enter your choice: ")
	print ""
	if (choice == "1"):
		print "Team Line-up"
		while (i < len(playerNames)):
			print(playerPos[i] + " " +  playerNames[i])
			i = i + 1
		i = 0
	elif(choice == "2"):
		print "Team Line-up "
		while(i < len(playerPos)):
			print(playerPos[i] + "   " +  playerNames[i].ljust(23) + playerCond[i].ljust(10))
			i = i + 1
		i = 0
	elif(choice == "3"):
		print "Team Line-up "
		print ""
		print "Pos  Name\t\t    Team Pos   | %Start PassYds PassTD PassInt RushYds RushTD RecYds RecTD RetTD Misc 2Pt FumLost"
		while(i < len(playerPos)):
			print(playerPos[i] + "   " +  playerNames[i].ljust(23) + playerCond[i].ljust(10) + " | " + playerStat[i])
			i = i + 1
		i = 0
	elif(choice == "4"):
		print "Exiting the program"	
		sys.exit(0)
	elif(choice == "5"):
		displayStats(username,reader, data, strList)
		indent()		
	else:
		print "Invalid choice"
		displayPlayers(reader, playerNames, playerPos, playerCond, playerStat, data, username, strList)

	displayPlayers(reader, playerNames, playerPos, playerCond, playerStat, data, username, strList)

def main():
	mainMenu()

def indent():

#print's blank lines to make the information easier to read and navigate.
	print ""
	print ""
	print ""
  


if __name__ == "__main__":
    main()
