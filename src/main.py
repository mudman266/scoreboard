# Josh Williams
# Last edit: 1/22/22
# main.py

import menu
import editSports


def main_sequence():
    # Show the menu
    userMenu = menu.Menu()
    option = userMenu.printMenu()

    # TODO - add a record to each team on the hockey list
    switcher = {
        1: editSports.Sports.showSports()
    }
    switcher.get(option)


if __name__ == "__main__":
    main_sequence()
