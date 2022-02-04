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
    def print_menu():
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
                settings.Settings.print_menu()
            elif int(decision) == 2:
                editSports.Sports.show_sports()
            elif int(decision) == 3:
                editSports.Sports.show_hockey_teams()
            elif int(decision) == 4:
                Menu.show_scores()
            elif int(decision) == 5:
                quit()
        else:
            print("Not a valid selection. Try again.")
            Menu.printMenu()

    @staticmethod
    def show_scores():

        Menu.update_files()

        # Parse the scores file
        my_settings = settings.Settings()
        curSettings = my_settings.getSettings()
        curPath = curSettings["pathToScoreBoard"]
        scoresFile = curPath + "/src/scores.json"
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

    @staticmethod
    def edit_teams():
        pass

    @staticmethod
    def update_files():
        # do we need to update our scores file - check settings file
        my_settings = settings.Settings()
        curSettings = my_settings.getSettings()
        curPath = curSettings["pathToScoreBoard"]
        lastUpdate = curSettings["lastUpdate"]

        # If lastUpdate value is blank or more than 15 mins in the past,
        # run the update and update the last update time
        timeMinus15Mins = datetime.timedelta(minutes=15)
        scoresFile = curPath + "/src/scores.json"
        if lastUpdate == ("") or (
            lastUpdate <= (datetime.datetime.timestamp(datetime.datetime.now() - timeMinus15Mins))):
            # Updating scores
            print("Updating scores...")

            # Build the URLs
            hockey_urls = [f"https://statsapi.web.nhl.com/api/v1/teams",
                        f"https://statsapi.web.nhl.com/api/v1/teams/12?expand=team.schedule.previous"
                        ]

            settingsFile = curPath + "/src/settings.json"

            hockey_files = [curPath + "/src/hockey.json",
            curPath + "/src/lastHurricaneGame.json"
            ]

            c = urllib3.PoolManager()

            # TODO: Read settings file and then change 'lastUpdate' to avoid losing all other info
            curSettings['lastUpdate'] = datetime.datetime.timestamp(datetime.datetime.now())
            a = open(settingsFile, 'w')
            json.dump(curSettings, a)
            a.close()
            for i in range(0, len(hockey_urls)):
                with c.request('GET', hockey_urls[i], preload_content=False) as res, open(hockey_files[i], 'wb')\
                as out_file:
                    shutil.copyfileobj(res, out_file)
        else:
            # Last update within 15 mins
            print(str(lastUpdate) + " was greater than " + str(
                datetime.datetime.timestamp(datetime.datetime.now() - timeMinus15Mins)))
            print("tminus15mins: " + str(timeMinus15Mins))
            print("Last update < 15 mins ago...skipping update.")