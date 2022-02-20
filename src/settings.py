import json
import collections

import menu


class Settings:

    def __init__(self):
        self.last_update = ''
        self.debugging = ''
        self.cur_path = ''

    @staticmethod
    def print_menu():
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
                newMenu.print_settings()
            elif int(decision) == 2:
                newMenu.edit_settings()
            elif int(decision) == 3:
                newMenu.exit_to_main()
        else:
            print("Not a valid selection. Try again.")
            Settings.printMenu()

    def __str__(self):
        return str(self.last_update)

    def edit_settings(self):
        # TODO - Implement changing of settings
        pass

    def exit_to_main(self):
        menu.Menu.print_menu()


    def get_settings(self):
        # Grab the local path from settings file
        _settingsFile = open('data/settings.json')
        settings = json.load(_settingsFile)
        _settingsFile.close()
        self.debugging = True if settings['debugging'] else False
        self.cur_path = settings['cur_path']
        self.last_update = settings['lastUpdate']
        return settings