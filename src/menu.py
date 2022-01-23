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
        print(f"{curDate.year}-{curDate.month}-{curDate.day}")

        # Build the URL
        scoreUrl = f"https://statsapi.web.nhl.com/api/v1/schedule?teamId=12&startDate=" \
                   f"{curDate.year}-{curDate.month}-{curDate.day}" \
                   f"&endDate=" \
                   f"{curDate.year}-{curDate.month}-{curDate.day - 5}"

        # Make the request and save the result
        c = urllib3.PoolManager()
        curSettings = settings.Settings.getSettings()
        curPath = curSettings["pathToScoreBoard"]
        scoresFile = curPath + "/src/scores.json"
        with c.request('GET', scoreUrl, preload_content=False) as res, open(scoresFile, 'wb') as out_file:
            shutil.copyfileobj(res, out_file)

        updatedScores = open(scoresFile)
        scores = json.load(updatedScores)
        print(scores)
