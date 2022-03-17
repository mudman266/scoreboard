# Josh Williams
# Last update: 1/22/22
# editSports.py

import urllib3, shutil
import json
import menu, settings

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
        curSettings = my_settings.getSettings()
        curPath = curSettings["pathToScoreBoard"]
        teams_file_path = curPath + "/src/hockey.json"

        subscribed_file_path = curPath + "/src/subscribed.json"
        with open(subscribed_file_path) as subscribed_file_stream:
            subscribed_file_json = json.load(subscribed_file_stream)

            with open(teams_file_path, 'r') as teams_file_stream:
                teams_file_json = json.load(teams_file_stream)

                numeric_label = 1

                for team in teams_file_json["teams"]:
                    if str(team["franchise"]["franchiseId"]) in subscribed_file_json["hockey"]:
                        print(f'{numeric_label}) [X] {team["name"]}')
                    else:
                        print(f'{numeric_label}) [ ] {team["name"]}')
                    numeric_label += 1
            teams_file_stream.close()
        subscribed_file_stream.close()

    @staticmethod
    def toggle_subscribe(group_name, team_id):
        my_settings = settings.Settings()
        curSettings = my_settings.getSettings()
        curPath = curSettings["pathToScoreBoard"]
        subscribed_file_path = curPath + "/src/subscribed.json"
        with open(subscribed_file_path, 'r') as subscribed_file_stream:
            subscribed_file_json = json.load(subscribed_file_stream)
            if team_id in subscribed_file_json[group_name]:
                subscribed_file_json[group_name].remove(team_id)
            else:
                subscribed_file_json[group_name].append(team_id)
        subscribed_file_stream.close()

        subscribed_file_writer = open(subscribed_file_path, 'w')
        subscribed_file_serialized = json.dumps(subscribed_file_json, indent=2)
        subscribed_file_writer.write(subscribed_file_serialized)

        if curSettings["debugging"] == True:
            print("Successfully toggled team.")