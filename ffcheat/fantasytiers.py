__author__ = 'Jared'

import requests
import re
import sys
import prettytable
from fantasypros import FantasyPros, FantasyProsException


class FantasyTiersException(Exception):
    pass


class FantasyTiers(object):
    tiers = None

    def __init__(self, url='https://s3-us-west-1.amazonaws.com/fftiers/out/current/text_Flex.txt'):
        self.url = url
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

    def get_single_player_data(self, playername):
        try:
            player_data = self.get_tier_number_for_player(playername)
            return player_data
        except IndexError:
            raise FantasyTiersException('Player Not Found')

    def get_tier_number_for_player(self, playername):
        for tier in self.tiers:
            if playername in tier['players']:
                return int(tier['tier'])
        return 100







