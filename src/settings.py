import json
import collections

import menu


class Settings:

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
        settings = Settings.getSettings()
        _localPath = settings['pathToScoreBoard']
        print(f"Local path: {_localPath}")
        self.printMenu()

    def editSettings(self):
        pass

    def exitToMain(self):
        menu.Menu.printMenu()

    @staticmethod
    def getSettings():
        # Grab the local path from settings file
        _settingsFile = open('settings.json')
        settings = json.load(_settingsFile)
        return settings