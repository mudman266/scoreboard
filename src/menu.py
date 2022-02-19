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
        my_settings.get_settings()
        scores_file = my_settings.cur_path + "/src/data/scores.json"
        updated_scores = open(scores_file, "r")
        scores = json.load(updated_scores)
        date = datetime.date.today()

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
            if my_settings.debugging == True:
                print(f"Trying index: {dateIndex}")
            awayTeamName = scores['dates'][0]['games'][0]['teams']['away']['team']['name']
        except IndexError:
            if debugging:
                print("Bad index.")
            dateIndex += 1
            if debugging:
                print(f"Increased to..{dateIndex}")

        awayTeamScore = scores['dates'][0]['games'][0]['teams']['away']['score']

        # ----- End Away Info -----

        # ----- Start Home Info -----

        homeTeamName = scores['dates'][0]['games'][0]['teams']['home']['team']['name']
        homeTeamScore = scores['dates'][0]['games'][0]['teams']['home']['score']

        # ----- End Home Info -----

        # ----- Start Game Info -----

        # Game date
        gameDate = scores['dates'][0]['date']
        gameDateFormatted = datetime.datetime.strftime(datetime.datetime.strptime(gameDate, '%Y-%m-%d'), '%m/%d/%Y')

        # ----- End Game Info -----

        # Format and display info
        print(f"Last Game...\n"
              f"Date: {gameDateFormatted}\n"
              f"{awayTeamName} - {awayTeamScore}\n"
              f"{homeTeamName} - {homeTeamScore}")

    @staticmethod
    def edit_teams():
        pass

    @staticmethod
    def update_files():
        # do we need to update our scores file - check settings file for the last update timestamp
        my_settings = settings.Settings()
        my_settings.get_settings()

        # If lastUpdate value is blank or more than 15 mins in the past,
        # run the update and update the last update time
        timeMinus15Mins = datetime.timedelta(minutes=15)
        scores_file = my_settings.cur_path + "/src/data/scores.json"
        if my_settings.last_update == ("") or (
            my_settings.last_update <= (datetime.datetime.timestamp(datetime.datetime.now() - timeMinus15Mins))):
            # Updating scores
            print("Updating scores...")

            # Build the URLs
            hockey_urls = [f"https://statsapi.web.nhl.com/api/v1/teams",
                           "https://statsapi.web.nhl.com/api/v1/schedule"
                        ]


            hockey_files = [my_settings.cur_path + "/src/data/hockey.json",
                            my_settings.cur_path + "/src/data/scores.json"
            ]

            c = urllib3.PoolManager()

            # TODO: Read settings file and then change 'lastUpdate' to avoid losing all other info
            my_settings.last_update = datetime.datetime.timestamp(datetime.datetime.now())
            a = open(my_settings.cur_path + "/src/data/settings.json", 'w')
            json.dump(my_settings.__dict__, a)
            a.close()
            for i in range(0, len(hockey_urls)):
                with c.request('GET', hockey_urls[i], preload_content=False) as res, open(hockey_files[i], 'wb')\
                as out_file:
                    shutil.copyfileobj(res, out_file)
        else:
            # Last update within 15 mins
            print(str(last_update) + " was greater than " + str(
                datetime.datetime.timestamp(datetime.datetime.now() - timeMinus15Mins)))
            print("tminus15mins: " + str(timeMinus15Mins))
            print("Last update < 15 mins ago...skipping update.")