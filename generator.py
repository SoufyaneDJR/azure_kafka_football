"""
The idea is to simulate a football league environnement
It will be generating in real time updates of the GAMEes in between two clubs in the same league, and generate via probability the scores
"""
from Team import Team
import time
import random
import json

GAME_LENGTH = 90
class Game:
    def __init__(self, home_team: Team, away_team: Team):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = 0
        self.away_score = 0
        self.current_minute = 0

    def simulate_minute(self):
        # Home team chance to score
        home_attack_prob = self.home_team.home_prob_att * (1 - self.away_team.away_prob_def)/(GAME_LENGTH/4)
        away_attack_prob = self.away_team.away_prob_att * (1 - self.home_team.home_prob_def)/(GAME_LENGTH/4)

        # Determine if home team scores
        if random.uniform(0,1) < home_attack_prob:
            self.home_score += 1

        # Determine if away team scores
        if random.uniform(0,1) < away_attack_prob:
            self.away_score += 1

    def print_score(self):
        print(f"Minute {self.current_minute}: {self.home_team.club_name} {self.home_score} - {self.away_team.club_name} {self.away_score}")

    def _update_json_file(self, home_team: Team, away_team: Team):
        """Updates the JSON file with the new team probabilities after a match."""
        # Load the existing data from the JSON file
        with open("Database/Team_stats.json", "r") as file:
            data = json.load(file)

        # Update the probabilities for the home team
        for team in data["teams"]:
            if team["club_name"] == home_team.club_name:
                team["home_prob_att"] = home_team.home_prob_att
                team["home_prob_def"] = home_team.home_prob_def
                team["away_prob_att"] = home_team.away_prob_att
                team["away_prob_def"] = home_team.away_prob_def

        # Update the probabilities for the away team
        for team in data["teams"]:
            if team["club_name"] == away_team.club_name:
                team["home_prob_att"] = away_team.home_prob_att
                team["home_prob_def"] = away_team.home_prob_def
                team["away_prob_att"] = away_team.away_prob_att
                team["away_prob_def"] = away_team.away_prob_def

        # Write the updated data back to the JSON file
        with open("Database/Team_stats.json", "w") as file:
            json.dump(data, file, indent=4)

        print(f"Probabilities for {home_team.club_name} and {away_team.club_name} have been updated successfully.")

    def update_probabilities(self, home_team:Team, away_team:Team):
        if self.current_minute == 90:
            if self.home_score > self.away_score:
                # Home team wins: increase home team's attacking probability slightly, decrease away team's defensive probability
                home_team.home_prob_att *= 1.005  # Increase by 5%
                away_team.away_prob_def *= 0.995  # Decrease by 5%

                # Decrease the away team's attacking probability to reflect a weaker performance
                away_team.away_prob_att *= 0.995  # Decrease by 3%

                # Check for a clean sheet
                if self.away_score == 0:
                    home_team.home_prob_def *= 1.005  # Increase defensive probability by 5%
                    print(f"{self.home_team.club_name} kept a clean sheet! Defense improved.")

                print(f"{self.home_team.club_name} wins! Probabilities updated.")
            
            elif self.home_score < self.away_score:
                # Away team wins: increase away team's attacking probability slightly, decrease home team's defensive probability
                away_team.away_prob_att *= 1.005  # Increase by 5%
                home_team.home_prob_def *= 0.995  # Decrease by 5%

                # Decrease the home team's attacking probability to reflect a weaker performance
                home_team.home_prob_att *= 0.995  # Decrease by 3%

                # Check for a clean sheet
                if self.home_score == 0:
                    away_team.away_prob_def *= 1.005  # Increase defensive probability by 5%
                    print(f"{self.away_team.club_name} kept a clean sheet! Defense improved.")

                print(f"{self.away_team.club_name} wins! Probabilities updated.")
            
            else:
                # Draw: slightly increase defensive and attacking probabilities for both teams to simulate balance
                home_team.home_prob_att *= 1.005  # Increase by 2%
                away_team.away_prob_att *= 1.005  # Increase by 2%
                home_team.home_prob_def *= 1.005  # Increase by 2%
                away_team.away_prob_def *= 1.005  # Increase by 2%

                # Check for clean sheets for both teams
                if self.home_score == 0:
                    away_team.away_prob_def *= 1.005  # Increase defensive probability by 5%
                    print(f"{self.away_team.club_name} kept a clean sheet! Defense improved.")
                if self.away_score == 0:
                    home_team.home_prob_def *= 1.005  # Increase defensive probability by 5%
                    print(f"{self.home_team.club_name} kept a clean sheet! Defense improved.")

                print("Match ends in a draw. Probabilities updated for both teams.")
            
            ## update fixtures.json
            self._update_json_file(home_team, away_team)


def get_team_stats(club_name) : 
    stats = None
    with open("Database/Team_stats.json", "r") as file_ : 
        stats = json.load(file_)
    teams = stats["teams"]
    for team in teams : 
        if team["club_name"] == club_name : 
            return Team(club_name, team["home_prob_att"],  team["home_prob_def"],  team["away_prob_att"],  team["away_prob_def"])

def generate(game:Game):
    # Simulate the game
    for minute in range(1, GAME_LENGTH + 1):
        game.current_minute = minute
        game.simulate_minute()  # Simulate one minute of the match
        game.print_score()      # Print the score every minute
        # time.sleep(0.1)           # Simulate real-time by sleeping for 1 second per minute

def gameweek(fixtures_file): 
    fixtures:json = None
    with open(fixtures_file, "r") as file_ : 
        fixtures = json.load(file_)
    
    for gameweek in fixtures.keys() : 
        for game in fixtures[gameweek] :
            # print(game) 
            home_team = get_team_stats(game["home_team"])
            away_team = get_team_stats(game["away_team"])
            # Create the game
            game = Game(home_team, away_team)
            # print(home_team, away_team)
            generate(game)
            game.update_probabilities(game.home_team, game.away_team) 
gameweek("Database/fixtures.json")