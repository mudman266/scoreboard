# Josh Williams
# Last edit: 1/22/22
# menu.py

import collections


class Menu(object):
    def __init__(self):
        pass

    menuOptions = {1: 'Add/Remove Sports', 2: 'Add/Remove Teams',
                   3: 'Show Scores'}
    selectedOption = 0

    def printMenu(self):
        # Prints the menu and returns a valid selection
        menuItems = collections.ChainMap(self.menuOptions)
        for key, val in menuItems.items():
            print(f"{key}: {val}")
        decision = input("Option: ")
        if int(decision) in menuItems:
            switcher = {
                1: settings.Settings.showMenu(),
                2: editSports.Sports.showSports()
            }
            switcher.get(decision)
        else:
            print("Not a valid selection. Try again.")
            self.printMenu()
