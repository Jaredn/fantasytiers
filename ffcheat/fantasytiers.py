__author__ = 'Jared'

import requests
import yaml
import re
import sys
import prettytable
from fantasypros import FantasyPros, FantasyProsException


class FantasyTiers(object):
    TEAM_YAML_LOC = 'my_teams_config.yml'
    teams = None
    tiers = None


    def __init__(self, url='https://s3-us-west-1.amazonaws.com/fftiers/out/current/text_Flex.txt'):
        self.url = url
        self.load_teams()
        self.get_fantasy_tiers()

    def get_fantasy_tiers(self):
        r = requests.get(self.url)

        tiers = r.content.split("\n")
        tier_object = []
        for tier in tiers:
            tier_num = None
            tier_players = None
            m = re.match('^Tier\s+(\d+):', tier)
            if m:
                tier_num = m.groups()[0]
            m = re.match('^.*:(.*)', tier)
            if m:
                tier_players = m.groups()[0]
            if tier_num is not None and tier_players is not None:
                tier_object.append({'tier': tier_num, 'players': tier_players})
        self.tiers = tier_object
        return tier_object

    def load_teams(self):
        with open(self.TEAM_YAML_LOC, 'r') as stream:
            self.teams = yaml.load(stream)

    def rank_players(self):
        ranked_players_list = []
        sorted_ranked_players_list = {}
        for index, team in enumerate(self.teams['teams']):
            ranked_players_list = []
            for player in self.teams['teams'][team]:
                player_tier = self.get_tier_number_for_player(player['name'])
                ranked_players_list.append({'name': player['name'], 'tier': player_tier, 'position': player['position']})
            sorted_ranked_players_list[team] = sorted(ranked_players_list, key=lambda k: k['tier'])
        return sorted_ranked_players_list

    def get_tier_number_for_player(self, playername):
        for tier in self.tiers:
            if playername in tier['players']:
                return int(tier['tier'])
        return 100


def main():
    FT = FantasyTiers()
    FP = FantasyPros()
    ranked_players_by_team = FT.rank_players()
    pt = prettytable.PrettyTable(['Team', 'Player', 'Position', 'Tier', 'FP Rank', 'Opp', 'FPBest', 'FPWorst', 'FPAvg', 'FPStd_Dev'])
    pt.align = 'r'
    for team, players in ranked_players_by_team.iteritems():
        player_string = ''
        for player in players:
            try:
                fp_player_data = FP.get_single_player_data(player['name'])
                fp_player_rank = str(fp_player_data[0])
                fp_player_name = str(fp_player_data[1])
                fp_player_opp = str(fp_player_data[2])
                fp_player_pos = str(fp_player_data[3])
                fp_player_best = str(fp_player_data[4])
                fp_player_worst = str(fp_player_data[5])
                fp_player_avg = str(fp_player_data[6])
                fp_player_stddev = str(fp_player_data[7])
            except FantasyProsException:
                fp_player_rank = 'N/A'
                fp_player_name = 'N/A'
                fp_player_opp = 'N/A'
                fp_player_pos = 'N/A'
                fp_player_best = 'N/A'
                fp_player_worst = 'N/A'
                fp_player_avg = 'N/A'
                fp_player_stddev = 'N/A'
            pt.add_row([team, '%s (%s)' % (player['name'], fp_player_name), fp_player_pos, player['tier'], fp_player_rank, fp_player_opp, fp_player_best, fp_player_worst, fp_player_avg, fp_player_stddev])
    print pt

if __name__ == '__main__':
    sys.exit(main())








