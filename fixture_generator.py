import json
import random
from datetime import datetime, timedelta

teams = None
with open("Database/Teams.json", "r") as f :
    teams = json.load(f)

def generate_fixtures(teams):
    fixture_list = {}
    gameweek = 1
    matches = []
    total_teams = len(teams)

    # Start date
    start_date = datetime(2024, 11, 9)

    # Generate all possible fixtures (home and away for each pair of teams)
    all_fixtures = []
    for i, home_team in enumerate(teams):
        for away_team in teams[i+1:]:
            all_fixtures.append((home_team["club_name"], away_team["club_name"]))
            all_fixtures.append((away_team["club_name"], home_team["club_name"]))

    # Shuffle fixtures to randomize their order
    random.shuffle(all_fixtures)

    # Create matches and assign to gameweeks
    for fixture in all_fixtures:
        date = (start_date + timedelta(weeks=gameweek - 1)).strftime('%Y-%m-%d') if len(matches) + 1 < 10 else (start_date + timedelta(weeks=gameweek - 1, days= 1)).strftime('%Y-%m-%d')
        match = {
            "match_id": f"{gameweek}_{len(matches) + 1}",
            "home_team": fixture[0],
            "away_team": fixture[1],
            "date": date,
            "time": f"{random.randint(18, 22)}:00"
        }
        matches.append(match)

        # After every week, increase the gameweek count
        if len(matches) % (total_teams // 2) == 0:  # one gameweek contains half the teams' home and away games
            fixture_list[f"gameweek_{gameweek}"] = matches
            gameweek += 1
            matches = []

    return fixture_list

# Generate the fixtures
fixtures = generate_fixtures(teams)

# Save to a JSON file
with open("Database/fixtures.json", "w") as f:
    json.dump(fixtures, f, indent=2)

print("Fixtures have been generated and saved to fixtures.json")
