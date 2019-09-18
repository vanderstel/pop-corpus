import os

import click

YEAR_LIST_FILE = 'year_list.txt'
OUTPUT_DIRECTORY = 'output/'

@click.command()
def cli():
    """ Analyze corpus files. """
    with open(YEAR_LIST_FILE, 'r') as file:
        for song in file.read().splitlines():
            year, name = song.split(' ')
            song_file = open(os.path.join(OUTPUT_DIRECTORY, name + '.txt'), 'r')
            for event in song_file.read().splitlines():
                onset, offset, _, _, stress, syllable = event.split(' ')
                print stress, syllable

                # eighth = timepoint.split('.')[1] in ['1250', '3750', '6250', '8750']
                # sixteenth = timepoint.split('.')[1] in ['0625', '1875', '3125', '4375', '5625', '6875', '8125', '9375']
                # TODO: define the syncopation types you want to test, and then
                # operationalize them here.
