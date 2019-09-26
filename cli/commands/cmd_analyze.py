import os
from collections import OrderedDict

import click

YEAR_LIST_FILE = 'year_list.txt'
OUTPUT_DIRECTORY = 'output/'



# VARS
# Just sandboxing right now

years = OrderedDict()


@click.command()
def cli():
    """ Analyze corpus files. """
    with open(YEAR_LIST_FILE, 'r') as file:
        for song in file.read().splitlines():
            year, name = song.split(' ')
            year = int(year)
            if year not in years:
                years[year] = {
                    'offbeats': 0,
                    'second_pos': 0,
                    'fourth_pos': 0
                }
            song_file = open(os.path.join(OUTPUT_DIRECTORY, name + '.txt'), 'r')
            for event in song_file.read().splitlines():
                onset, offset, _, _, stress, syllable = event.split(' ')
                duration = float(offset) - float(onset)
                eighth = onset.split('.')[1] in ['125', '375', '625', '875']
                fourth_position = onset.split('.')[1] in [ ] and duration > 0.125
                # years[year]['total'] += 1
                # if eighth:
                #     years[year]['offbeats'] += 1
                # if second_position:
                #     years[year]['second_pos'] += 1
                # if fourth_position:
                #     years[year]['fourth_pos'] += 1

    for year, data in years.iteritems():
        # ratio = float(data['syncs']) / float(data['offbeats'])
        print year, data


    # What are the different syncopation types outlined by Temp & Condit-Schultz?
    # Define each here, so hunting for them.
    # Anchored vs. unanchored
    # Continued vs. curtailed
    # Approached by leap vs. step
    # Approached by ascending int vs. descending int
    #
