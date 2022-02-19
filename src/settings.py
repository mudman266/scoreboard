import json
import collections

import menu


class Settings:

    def __init__(self):
        self.lastUpdate = ''
        self.debugging = ''
        self.cur_path = ''

    @staticmethod
    def printMenu():
        # Prints the menu and returns a valid selection
        # Menu Options
        menuOptions = {1: 'View Settings', 2: 'Edit Settings',
                       3: 'Exit Settings'}

        menuItems = collections.ChainMap(menuOptions)
        for key, val in menuItems.items():
            print(f"{key}: {val}")
        decision = input("Option: ")
        if int(decision) in menuItems:
            newMenu = Settings()
            if int(decision) == 1:
                newMenu.printSettings()
            elif int(decision) == 2:
                newMenu.editSettings()
            elif int(decision) == 3:
                newMenu.exitToMain()
        else:
            print("Not a valid selection. Try again.")
            Settings.printMenu()

    def printSettings(self):
        # Local path
        settings = Settings.getSettings()
        _localPath = settings['pathToScoreBoard']
        print(f"Local path: {_localPath}")

        # Back to the menu
        self.printMenu()

    def editSettings(self):
        pass

    def exitToMain(self):
        menu.Menu.printMenu()

    def get_settings(self):
        # Grab the local path from settings file
        _settingsFile = open('settings.json')
        settings = json.load(_settingsFile)
        _settingsFile.close()
        self.debugging = True if settings['debugging'] == True else False
        self.cur_path = settings['cur_path']
        self.last_update = settings['lastUpdate']
        return settings