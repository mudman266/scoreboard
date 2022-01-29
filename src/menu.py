# Josh Williams
# Last edit: 1/22/22
# menu.py

import collections
import datetime
import json
import shutil
import urllib3

# import pages
import editSports
import settings

debugging = True


class Menu(object):
    def __init__(self):
        pass

    @staticmethod
    def printMenu():
        # Prints the menu and runs a valid selection

        menuOptions = {1: 'Settings',
                       2: 'Add/Remove Sports',
                       3: 'Add/Remove Teams',
                       4: 'Show Scores',
                       5: 'Exit'
                       }
        menuItems = collections.ChainMap(menuOptions)
        for key, val in menuItems.items():
            print(f"{key}: {val}")
        decision = input("Option: ")
        if int(decision) in menuItems:
            if int(decision) == 1:
                settings.Settings.printMenu()
            elif int(decision) == 2:
                editSports.Sports.showSports()
            elif int(decision) == 3:
                pass
            elif int(decision) == 4:
                Menu.showScores()
            elif int(decision) == 5:
                quit()
        else:
            print("Not a valid selection. Try again.")
            Menu.printMenu()

    @staticmethod
    def showScores():
        # get the date
        curDate = datetime.datetime.now()

        # do we need to update our scores file
        c = urllib3.PoolManager()
        curSettings = settings.Settings.getSettings()
        curPath = curSettings["pathToScoreBoard"]
        lastUpdate = curSettings["lastUpdate"]

        # Build the URL
        scoreUrl = f"https://statsapi.web.nhl.com/api/v1/teams/12?expand=team.schedule.previous"

        # Make the request and save the result

        # If lastUpdate value is blank or more than 15 mins in the past,
        # run the update and update the last update time
        timeMinus15Mins = datetime.timedelta(minutes=15)
        scoresFile = curPath + "/src/scores.json"
        if lastUpdate == ("") or (lastUpdate <= (datetime.datetime.timestamp(datetime.datetime.now() - timeMinus15Mins))):
            # Updating scores
            print("Updating scores...")

            settingsFile = curPath + "/src/settings.json"
            curSettings['lastUpdate'] = datetime.datetime.timestamp(datetime.datetime.now())
            a = open(settingsFile, 'w')
            json.dump(curSettings, a)
            a.close()
            with c.request('GET', scoreUrl, preload_content=False) as res, open(scoresFile, 'wb') as out_file:
                shutil.copyfileobj(res, out_file)
        else:
            # Last update within 15 mins
            print(str(lastUpdate) + " was greater than " + str(datetime.datetime.timestamp(datetime.datetime.now() - timeMinus15Mins)))
            print("tminus15mins: " + str(timeMinus15Mins))
            print("Last update < 15 mins ago...skipping update.")


        # Parse the scores file
        updatedScores = open(scoresFile, "r")
        scores = json.load(updatedScores)
        date = datetime.date.today()
        found = False

        # ----- Start Away Info -----

        dateIndex = 0
        awayTeamName = ""
        awayTeamScore = ""

        # TODO: Break the below code into two functions in a class
        # TODO: 1) Find the dateindex
        # TODO: 2) Get scores for the last game of a team

        # Loop until we find a valid score
        # while found is False:
        try:
            if debugging:
                print(f"Trying index: {dateIndex}")
            awayTeamName = scores['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['away']['team']['name']
            found = True
        except IndexError:
            if debugging:
                print("Bad index.")
            dateIndex += 1
            if debugging:
                print(f"Increased to..{dateIndex}")

        awayTeamScore = scores['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['away']['score']

        # ----- End Away Info -----

        # ----- Start Home Info -----

        homeTeamName = scores['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['home']['team']['name']
        homeTeamScore = scores['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['teams']['home']['score']

        # ----- End Home Info -----

        # ----- Start Game Info -----

        # Game date
        gameDate = scores['teams'][0]['previousGameSchedule']['dates'][0]['date']
        gameDateFormatted = datetime.datetime.strftime(datetime.datetime.strptime(gameDate, '%Y-%m-%d'), '%m/%d/%Y')

        # ----- End Game Info -----

        # Format and display info
        print(f"Last Game...\n"
              f"Date: {gameDateFormatted}\n"
              f"{awayTeamName} {awayTeamScore}\n"
              f"{homeTeamName} {homeTeamScore}")
