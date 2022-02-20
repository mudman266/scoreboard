import team


class Game:

    def __init__(self, home_team_id, away_team_id):
        home_team = team.Team()
        home_team.get_team(home_team_id)

        away_team = team.Team()
        away_team.get_team(away_team_id)

        self.home_team = home_team
        self.away_team = away_team