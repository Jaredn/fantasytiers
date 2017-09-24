__author__ = 'Jared'

import sys
import prettytable
import yaml
from fantasypros import FantasyPros, FantasyProsException
from fantasytiers import FantasyTiers, FantasyTiersException
from draftkings import DraftKings, DraftKingsException

# models
from .player_model import PlayerModel

def load_teams(yaml_loc):
    with open(yaml_loc, 'r') as stream:
        local_teams_dict = yaml.load(stream)
        local_teams = {}
        for team in local_teams_dict['teams']:
            local_teams[team] = []
            for player in local_teams_dict['teams'][team]:
                local_teams[team].append(PlayerModel(player))
        return local_teams


def get_player_data_from_all_sources(player_object, FT, FP, DK=None):
    """
    :type FT: FantasyTiers
    :type FP: FantasyPros
    :type DK: DraftKings
    :type player_object: PlayerModel
    :param player_object:
    :return:
    """
    try:
        ft_data = FT.get_single_player_data(player_object.name)
        player_object.ft_tier = ft_data  # Fantasy Tiers only returns a tier number.
    except FantasyTiersException:
        pass

    try:
        fp_data = FP.get_single_player_data(player_object.name)
        player_object.fp_rank = int(fp_data[0])
        player_object.fp_name = str(fp_data[1])
        player_object.fp_opp = str(fp_data[2])
        player_object.fp_position = str(fp_data[3])
        player_object.fp_best = int(fp_data[4])
        player_object.fp_worst = int(fp_data[5])
        player_object.fp_avg = float(fp_data[6])
        player_object.fp_std_dev = float(fp_data[7])
    except FantasyProsException:
        pass

    try:
        dk_data = DK.get_single_player_data(player_object.name)
        player_object.dk_salary = dk_data['Salary']
        player_object.dk_avg_ppg = dk_data['AvgPointsPerGame']
    except DraftKingsException:
        pass


def rank_players_in_playerlist(playerlist):
    """
    :type playerlist: list[PlayerModel]
    :param playerlist:
    :return:
    """
    playerlist.sort(key=lambda x: x.fp_rank)
    return playerlist


def main():
    TEAM_YAML_LOC = 'my_teams_config.yml'
    local_teams = load_teams(TEAM_YAML_LOC)
    FT = FantasyTiers()
    FP = FantasyPros()
    DK = DraftKings()  # Data needs to be downloaded as CSV for league you care about.  Save as DKSalaries.csv.
    print('local teams = ', local_teams)
    print('== get player data test ==\n')

    # iterate over local_teams dictionary, and fill in all player data to the player object models.
    for team, playerlist in local_teams.iteritems():
        for player in playerlist:
            get_player_data_from_all_sources(player, FT, FP, DK)

    ### We have all player data now ###

    # Sort each team's player list
    for team, playerlist in local_teams.iteritems():
        playerlist = rank_players_in_playerlist(playerlist)

    # Team Lists have now been sorted.  Lets print the data.

    for team, playerlist in local_teams.iteritems():
        pt = prettytable.PrettyTable(['Team', 'Player', 'Position', 'Tier', 'FP Rank', 'Opp', 'FPBest', 'FPWorst', 'FPAvg', 'FPStd_Dev', 'DK_Salary', 'DK_Avg_PPG'])
        pt.align = 'r'
        for player in playerlist:
            player = player
            """
            :type player: PlayerModel
            """
            pt.add_row([
                team,
                player.name,
                player.fp_position,
                player.ft_tier,
                player.fp_rank,
                player.fp_opp,
                player.fp_best,
                player.fp_worst,
                player.fp_avg,
                player.fp_std_dev,
                player.dk_salary,
                player.dk_avg_ppg
            ])
        print(pt)

if __name__ == '__main__':
    sys.exit(main())
