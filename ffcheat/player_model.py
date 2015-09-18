__author__ = 'Jared'

class PlayerModel:
    """
    Class defining what a player object should contain
    """
    name = None             # player name
    team = None             # team player plays for (Example: Minnesota Vikings)
    team_short_name = None  # Abbreviated team name
    team_position = None    # actual position on the real team (example: QB1, RB2, WR2, etc)

    # Fantasy Tiers Data
    ft_tier = None

    # Fantasy Pros Data
    fp_rank = None
    fp_name = None
    fp_opp = None
    fp_position = None
    fp_best = None
    fp_worst = None
    fp_avg = None
    fp_std_dev = None

    def __init__(self, playername):
        self.name = playername

    def __str__(self):
        return "PlayerModel(%s)(%s)" % (self.name, self.fp_rank)

    def __repr__(self):
        return "PlayerModel(%s)(%s)" % (self.name, self.fp_rank)
