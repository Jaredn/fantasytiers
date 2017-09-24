__author__ = 'Jared'

import requests
from lxml import html


class FantasyProsException(Exception):
    pass


class FantasyPros(object):
    fp_data = None

    def __init__(self, rankings_chart='qb-flex'):
        self.url = 'http://www.fantasypros.com/nfl/rankings/%s.php' % rankings_chart
        self.fp_data = self.get_fantasy_pros_data()

    def get_fantasy_pros_data(self):
        r = requests.get(self.url)
        tree = html.fromstring(r.text)
        # players = tree.xpath('//*[@id="data"]/tbody/tr[*]/td[2]/div[*]/a[1]/text()')

        xpath1 = '//*[@id="data"]/tbody/tr'
        rows = tree.xpath(xpath1)
        data = list()
        for index, row in enumerate(rows):
            # I have no fucking clue why, but 50 ALWAYS errors out on every list.  All players still show up.
            if index is not 50:
                initial_data = [c.text_content() for c in row.getchildren()]
                # 2015-10-05 i commented this block out - apparently i no longer need the hack to get player names.
                # print initial_data
                # # player name is a link, so we grab its text individually inside the <a> element and update the list.
                # if row[1][0][0] is not None:
                #     playername = row[1][0][0].text
                #     initial_data[1] = playername
                data.append(initial_data)
        return data

    def get_single_player_data(self, playername):
        try:
            player_data = [e for e in self.fp_data if e[1] is not None and playername in e[1]][0] #last [0] is just so its not a list of lists.  Just the first list that matched.
        except IndexError:
            raise FantasyProsException('Player Not Found')
        return player_data
