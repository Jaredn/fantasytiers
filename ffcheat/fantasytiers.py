__author__ = 'Jared'

import requests
import yaml
import re
import sys
import prettytable


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
    ranked_players_by_team = FT.rank_players()
    pt = prettytable.PrettyTable(['Team', 'Ranked Players (WR/RB Combined)'])
    for team, players in ranked_players_by_team.iteritems():
        player_string = ''
        for player in players:
            player_string += '%s - Tier %s - %s\n' % (player['name'], player['tier'], player['position'])
        pt.add_row([team, player_string])
    print pt

if __name__ == '__main__':
    sys.exit(main())








