# Josh Williams
# Last update: 1/22/22
# editSports.py

import urllib3, shutil


class Sports:

    def __init__(self):
        pass

    @staticmethod
    def showSports():
        print(f"Showing sports....")
        # NHL Hockey
        Sports.showHockeyTeams()

    @staticmethod
    def showHockeyTeams():
        NHLurl = 'https://statsapi.web.nhl.com/api/v1/teams'

        # TODO - Update to use a env variable for the save location
        c = urllib3.PoolManager()
        NHLFile = 'c:/projects/python/scoreboard/src/hockey.json'
        with c.request('GET', NHLurl, preload_content=False) as res, open(NHLFile, 'wb') as out_file:
            shutil.copyfileobj(res, out_file)
