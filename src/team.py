import settings
import json


class Team:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.location_and_team_name = ''
        self.location = ''
        self.team_name = ''
        self.abbreviation = ''
        self.venue_name = ''
        self.timezone = ''
        self.timezone_offset = ''
        self.division = ''
        self.franchise_id = 00
        self.score = 00

    def get_team(self, id=None, team_name=None):
        # Will set the team object from looking at hockey.json. Provide an ID OR a team_name (ie cardinals).
        # If both are provided the ID takes priority
        my_settings = settings.Settings()
        my_settings.get_settings()
        teams_file_path = my_settings.cur_path + "/src/data/hockey.json"

        with open(teams_file_path, 'r') as teams_file_stream:
            teams_file_json = json.load(teams_file_stream)
            for team in teams_file_json["teams"]:
                if id is not None:
                    if team['id'] == id:
                        self.id = team['id']
                        self.name = team['name']
                        self.location_and_team_name = team['name']
                        self.location = team['locationName']
                        self.team_name = team['teamName']
                        self.abbreviation = team['abbreviation']
                        self.venue_name = team['venue']['name']
                        self.timezone = team['name']
                        self.timezone_offset = team['venue']['timeZone']['offset']
                        self.division = team['division']['id']
                        self.franchise_id = team['franchise']['franchiseId']
                        if my_settings.debugging == True:
                            print(f"Franchise ID: {self.franchise_id}")
                elif team_name is not None:
                    if str(lower(team['team_name'])) == str(lower(team_name)):
                        self.id = team['id']
                        self.name = team['name']
                        self.location_and_team_name = team['name']
                        self.location = team['locationName']
                        self.team_name = team['teamName']
                        self.abbreviation = team['abbreviation']
                        self.venue_name = team['venue']['name']
                        self.timezone = team['name']
                        self.timezone_offset = team['venue']['timeZone']['offset']
                        self.division = team['division']['id']
                        self.franchise_id = team['franchise']['franchiseId']
                        if my_settings.debugging == True:
                            print(f"Franchise ID: {self.franchise_id}")
        teams_file_stream.close()
        return self
