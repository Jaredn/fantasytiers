__author__ = 'Jared'

import sys
import prettytable
import yaml
from fantasypros import FantasyPros, FantasyProsException
from fantasytiers import FantasyTiers, FantasyTiersException

# models
from player_model import  PlayerModel

def load_teams(yaml_loc):
    with open(yaml_loc, 'r') as stream:
        local_teams_dict = yaml.load(stream)
        local_teams = {}
        for team in local_teams_dict['teams']:
            local_teams[team] = []
            for player in local_teams_dict['teams'][team]:
                local_teams[team].append(PlayerModel(player))
        return local_teams


def get_player_data_from_all_sources(player_object, FT, FP):
    """
    :type FT: FantasyTiers
    :type FP: FantasyPros
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
    print 'local teams = ', local_teams
    print '== get player data test ==\n'

    # iterate over local_teams dictionary, and fill in all player data to the player object models.
    for team, playerlist in local_teams.iteritems():
        for player in playerlist:
            get_player_data_from_all_sources(player, FT, FP)

    ### We have all player data now ###

    # Sort each team's player list
    for team, playerlist in local_teams.iteritems():
        playerlist = rank_players_in_playerlist(playerlist)

    # Team Lists have now been sorted.  Lets print the data.

    for team, playerlist in local_teams.iteritems():
        pt = prettytable.PrettyTable(['Team', 'Player', 'Position', 'Tier', 'FP Rank', 'Opp', 'FPBest', 'FPWorst', 'FPAvg', 'FPStd_Dev'])
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
                player.fp_std_dev
            ])
        print pt





    # ranked_players_by_team = FT.rank_players()
    #
    # for team, players in ranked_players_by_team.iteritems():
    #     pt = prettytable.PrettyTable(['Team', 'Player', 'Position', 'Tier', 'FP Rank', 'Opp', 'FPBest', 'FPWorst', 'FPAvg', 'FPStd_Dev'])
    #     pt.align = 'r'
    #     player_string = ''
    #     for player in players:
    #         try:
    #             fp_player_data = FP.get_single_player_data(player['name'])
    #             fp_player_rank = str(fp_player_data[0])
    #             fp_player_name = str(fp_player_data[1])
    #             fp_player_opp = str(fp_player_data[2])
    #             fp_player_pos = str(fp_player_data[3])
    #             fp_player_best = str(fp_player_data[4])
    #             fp_player_worst = str(fp_player_data[5])
    #             fp_player_avg = str(fp_player_data[6])
    #             fp_player_stddev = str(fp_player_data[7])
    #         except FantasyProsException:
    #             fp_player_rank = 'N/A'
    #             fp_player_name = 'N/A'
    #             fp_player_opp = 'N/A'
    #             fp_player_pos = 'N/A'
    #             fp_player_best = 'N/A'
    #             fp_player_worst = 'N/A'
    #             fp_player_avg = 'N/A'
    #             fp_player_stddev = 'N/A'
    #         pt.add_row([team, '%s (%s)' % (player['name'], fp_player_name), fp_player_pos, player['tier'], fp_player_rank, fp_player_opp, fp_player_best, fp_player_worst, fp_player_avg, fp_player_stddev])
    #     print pt

if __name__ == '__main__':
    sys.exit(main())
