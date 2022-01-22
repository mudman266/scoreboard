import json

class Settings:
    # Menu Options
    menuOptions = {1: 'View Settings', 2: 'Edit Settings',
                   3: 'Exit Settings'}

    # Grab the local path from settings file
    _settingsFile = json.loads('settings.json')
    _localPath = _settingsFile[pathToScoreBoard]

    def printMenu(self):
        # Prints the menu and returns a valid selection
        menuItems = collections.ChainMap(self.menuOptions)
        for key, val in menuItems.items():
            print(f"{key}: {val}")
        decision = input("Option: ")
        if int(decision) in menuItems:
            switcher = {
                1: self.printSettings(),
                2: self.editSettings(),
                3: self.exitToMain()
            }
            switcher.get(decision)
        else:
            print("Not a valid selection. Try again.")
            self.printMenu()

    def printSettings(self):
        print(f"Local path: {self._localPath}")

    def editSettings(self):
        pass

    def exitToMain(self):
        pass