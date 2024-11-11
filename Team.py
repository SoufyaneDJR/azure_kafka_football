class Team:
    def __init__(
        self, club_name, home_prob_att, home_prob_def, away_prob_att, away_prob_def
    ):
        self.club_name = club_name
        self.home_prob_att = home_prob_att
        self.home_prob_def = home_prob_def
        self.away_prob_att = away_prob_att
        self.away_prob_def = away_prob_def

    def __str__(self):
        return (
            f"===============================\n"
            f"|{self.club_name:^29}|\n"
            f"===============================\n"
            f"| Home Attacking:   {self.home_prob_att:.2f}      |\n"
            f"| Home Defending:   {self.home_prob_def:.2f}      |\n"
            f"|-----------------------------|\n"
            f"| Away Attacking:   {self.away_prob_att:.2f}      |\n"
            f"| Away Defending:   {self.away_prob_def:.2f}      |\n"
            f"===============================\n"
        )