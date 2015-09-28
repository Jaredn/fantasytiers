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

    # DraftKings Data
    dk_salary = None
    dk_avg_ppg = None

    def __init__(self, playername):
        self.name = playername

    def __str__(self):
        return "%s(%s)" % (self.__class__, self.name)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
