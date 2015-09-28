__author__ = 'Jared'

import requests
from lxml import html

import csv


class DraftKingsException(Exception):
    pass


class DraftKings(object):
    def __init__(self):
        self.url = ''
        self.salaries = []
        self.load_salaries()

    def get_single_player_data(self, playername):
        try:
            player_data = [row for row in self.salaries if playername in row['Name']][0] #0 on the end for single row returned.
        except IndexError:
            raise DraftKingsException('Player Not Found')
        return player_data

    def load_salaries(self, filename='/Users/Jared/PycharmProjects/ffcheat/ffcheat/DKSalaries.csv'):
        self.salaries = []
        with open(filename, 'rb') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.salaries.append(row)




