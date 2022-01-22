import json
import collections


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
            switcher = {
                1: newMenu.printSettings(),
                2: newMenu.editSettings(),
                3: newMenu.exitToMain()
            }
            switcher.get(decision)
        else:
            print("Not a valid selection. Try again.")
            self.printMenu()

    def printSettings(self):
        # Grab the local path from settings file
        _settingsFile = open('settings.json')
        settings = json.load(_settingsFile)
        _localPath = settings['pathToScoreBoard']
        print(f"Local path: {_localPath}")

    def editSettings(self):
        pass

    def exitToMain(self):
        pass