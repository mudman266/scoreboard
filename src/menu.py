# Josh Williams
# Last edit: 1/22/22
# menu.py

import collections
import settings
import editSports


class Menu(object):
    def __init__(self):
        pass

    menuOptions = {1: 'Settings',
                   2: 'Add/Remove Sports',
                   3: 'Add/Remove Teams',
                   4: 'Show Scores'
                   }
    selectedOption = 0

    def printMenu(self):
        # Prints the menu and runs a valid selection
        menuItems = collections.ChainMap(self.menuOptions)
        for key, val in menuItems.items():
            print(f"{key}: {val}")
        decision = input("Option: ")
        if int(decision) in menuItems:
            switcher = {
                1: settings.Settings.printMenu(),
                2: editSports.Sports.showSports()
            }
            switcher.get(decision)
        else:
            print("Not a valid selection. Try again.")
            self.printMenu()
