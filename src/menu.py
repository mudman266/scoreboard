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
import game

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
        subscribed_teams = open(my_settings.cur_path + "/src/data/subscribed.json", "r")
        subscribed_team_ids = json.load(subscribed_teams)

        subscribed_team_games = []

        # TODO: Get scores for the last game of a team
        for game_score in scores['dates'][0]['games']:
            if (game_score['teams']['away']['team']['id'] in subscribed_team_ids["hockey"]) or (game_score['teams']['home']['team']['id'] in subscribed_team_ids["hockey"]):
                valid_game = game.Game(game_score['teams']['home']['team']['id'], game_score['teams']['away']['team']['id'])

                valid_game.home_team.score = game_score['teams']['home']['score']
                valid_game.away_team.score = game_score['teams']['away']['score']

                gameDate = datetime.datetime.strptime(game_score["gameDate"], "%Y-%m-%dT%H:%M:%SZ")
                valid_game.date = gameDate.strftime("%m-%d-%Y")

                subscribed_team_games.append(valid_game)

        print("Recent Games:\n")

        for subscribed_game in subscribed_team_games:
            # Format and display info
            print(f"Date: {subscribed_game.date}\n"
                  f"{subscribed_game.away_team.name} - {subscribed_game.away_team.score}\n"
                  f"{subscribed_game.home_team.name} - {subscribed_game.home_team.score}\n")

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
        if my_settings.last_update == ("") or (
            my_settings.last_update <= (datetime.datetime.timestamp(datetime.datetime.now() - timeMinus15Mins))):

            # Updating scores
            print("Updating scores...")

            # Build the URLs
            hockey_urls = [f"https://statsapi.web.nhl.com/api/v1/teams",
                           f"https://statsapi.web.nhl.com/api/v1/schedule"
                        ]

            # Where to store the files from the urls
            hockey_files = [my_settings.cur_path + "/src/data/hockey.json",
                            my_settings.cur_path + "/src/data/scores.json"
            ]

            c = urllib3.PoolManager()

            # Update settings.last_update then save to the settings file
            my_settings.last_update = datetime.datetime.timestamp(datetime.datetime.now())
            a = open(my_settings.cur_path + "/src/data/settings.json", 'w')
            json.dump(my_settings.__dict__, a)
            a.close()

            # Get the files from the URLs
            for i in range(0, len(hockey_urls)):
                with c.request('GET', hockey_urls[i], preload_content=False) as res, open(hockey_files[i], 'wb')\
                as out_file:
                    shutil.copyfileobj(res, out_file)
        else:
            # Last update within 15 mins
            if my_settings.debugging == True:
                print(str(my_settings.last_update) + " was greater than " + str(
                    datetime.datetime.timestamp(datetime.datetime.now() - timeMinus15Mins)))
            print("Last update < 15 mins ago...skipping update.")