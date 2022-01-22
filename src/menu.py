# Josh Williams
# Last edit: 1/22/22
# menu.py

import collections
import settings
import editSports

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
                pass
            elif int(decision) == 5:
                quit()
        else:
            print("Not a valid selection. Try again.")
            Menu.printMenu()
