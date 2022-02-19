# Josh Williams
# Last update: 1/22/22
# editSports.py

import urllib3, shutil
import json
import menu, settings, team

class Sports:

    def __init__(self):
        pass

    @staticmethod
    def show_sports():
        print(f"Showing sports....")
        # TODO: Print menu of sports and teams with ability to enable/disable team
        pass


    @staticmethod
    def show_hockey_teams():
        menu.Menu.update_files()
        my_settings = settings.Settings()
        my_settings.get_settings()
        teams_file_path = my_settings.cur_path + "/src/hockey.json"
        subscribed_file_path = my_settings.cur_path + "/src/subscribed.json"

        numeric_label = 1

        teams_file_stream = open(teams_file_path,)
        teams_file_json = json.load(teams_file_stream)

        subscribed = open(subscribed_file_path)
        subscribed_file_json = json.load(subscribed)

        for team_entry in teams_file_json["teams"]:
            team_obj = team.Team()
            team_obj.get_team(team_entry['id'])
            if team_obj.franchise_id in subscribed_file_json["hockey"]:
                print(f'{numeric_label}) [X] {team_obj.name}')
            else:
                print(f'{numeric_label}) [ ] {team_obj.name}')
            numeric_label += 1


        # TODO - The choice needs to find the franchiseId of that team and add toggle it instead of list item number
        Sports.toggle_subscribe("hockey", input("Choice: "))

    @staticmethod
    def toggle_subscribe(group_name, team_id):
        # Toggles the presence of the team's franchiseID (converted from team_id) on subscribed.json
        team_obj = team.Team()
        team_obj.get_team(int(team_id))

        # Open the subscribed file
        my_settings = settings.Settings()
        my_settings.get_settings()
        subscribed_file_path = my_settings.cur_path + "/src/subscribed.json"

        subscribed_file = open(subscribed_file_path, 'r')
        subscribed_file_json = json.load(subscribed_file)

        # Toggle
        if team_obj.franchise_id in subscribed_file_json[group_name]:
            if my_settings.debugging == True:
                print(f'Removing {team_obj.name} from {group_name}')
            subscribed_file_json[group_name].remove(team_obj.franchise_id)
        else:
            if my_settings.debugging == True:
                print(f'Adding {team_obj.name} to {group_name}')
            subscribed_file_json[group_name].append(team_obj.franchise_id)

        # Update file
        subscribed_file_writer = open(subscribed_file_path, 'w')
        subscribed_file_serialized = json.dumps(subscribed_file_json, indent=2)
        subscribed_file_writer.write(subscribed_file_serialized)

        if my_settings.debugging == True:
            print(f"Successfully toggled {team_obj.name}.")