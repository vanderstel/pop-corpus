"""
Combines lyric files from the lyrics/ directory with
the matching transcription files from the transcriptions/ directory.
generating a file in the output/ directory.

(Based on work by Adam Waller.)
"""

import os
import csv
import itertools
import subprocess

import click

import dictionary
from utils import skip_comment_generator, format_word


LYRICS_DIRECTORY = 'lyrics/'
TRANSCRIPTIONS_DIRECTORY = 'transcriptions/'
OUTPUT_DIRECTORY = 'output/'

PERL_SCRIPT = 'cli/scripts/process-duration.pl'  # D.T.


@click.command()
def cli():
    """ Generate corpus files. (TODO: update to Python 3.8)"""
    for file in os.listdir(LYRICS_DIRECTORY):
        if not file.endswith('.txt'):
            continue

        note_list = generate_note_list(file)
        stress_list = generate_stress_list(file)
        with open(OUTPUT_DIRECTORY + file, 'w') as output_file:
            i = 0
            while True:
                try:
                    unit, syllable = stress_list[i]
                    output_file.write(
                        '{} {} {}\n'.format(note_list[i], unit, syllable))
                except:
                    break
                i = i + 1


def generate_note_list(file):
    """
    Use Temperley's Perl script to generate note list from transcription file.
    Return a list of note events.
    """
    if os.path.exists(TRANSCRIPTIONS_DIRECTORY + file):
        process = subprocess.Popen(
            [
                'perl', PERL_SCRIPT,
                '3', '0',
                 TRANSCRIPTIONS_DIRECTORY + file
            ],
            stdout=subprocess.PIPE)

        output, _ = process.communicate()
        return output.decode('utf-8').split('\n')


def generate_stress_list(file):
    """
    Given a lyrics file, return a list of stress events in this format:
        [stress, WORD[syllable_number]]
        E.g., [1, 'NOTHING[1]']
    """
    stress_list = []
    lyric_list = []
    with open(LYRICS_DIRECTORY + file, 'r') as lyric_file:
        for line in skip_comment_generator(lyric_file): # skip comments
            line = format_word(line)
            lyric_list.append(line.split())

    for word in list(itertools.chain.from_iterable(lyric_list)):
        try:
            emph_list = dictionary.lookup(word)
            for i in range(len(emph_list)):
                stress_list.append((emph_list[i], word + '[{}]'.format(i + 1)))
        except KeyError:
            continue
    return stress_list
