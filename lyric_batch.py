"""
Runs all lyrics files within a directory through the CMU dictionary
and returns output files of each.

Modified by Joseph VanderStel; based on work by Adam Waller.
"""

import os
import csv
import itertools
import subprocess

import stress


LYRICS_DIRECTORY = 'lyrics/'
TRANSCRIPTIONS_DIRECTORY = 'transcriptions/'
OUTPUT_DIRECTORY = 'output/'

def generate_note_list(file):
    """
    Use Temperley's Perl script to generate note list from transcription file.
    Return a list of note events.
    """
    if os.path.exists(TRANSCRIPTIONS_DIRECTORY + file):
        process = subprocess.Popen(
            [
                'perl', 'process-duration.pl',
                '3', '0',
                 TRANSCRIPTIONS_DIRECTORY + file
            ],
            stdout=subprocess.PIPE)

        output, _ = process.communicate()
        return output.split('\n')




def generate_stress_list(file):
    """
    Given a lyrics file, return a list of stress events in this format:
        [stress, WORD[syllable_number]]
        E.g., [1, 'NOTHING[1]']
    """
    stress_list = []
    lyric_list = []
    with open(LYRICS_DIRECTORY + file, 'rb') as lyric_file:
        for line in stress.skip_comment_generator(lyric_file): # skip comments
            line = stress.format_word(line)
            lyric_list.append(line.split())

    for word in list(itertools.chain.from_iterable(lyric_list)):
        try:
            emph_list = stress.dictionary[word]
            for i in range(len(emph_list)):
                stress_list.append((emph_list[i], word + '[{}]'.format(i + 1)))
        except KeyError:
            continue
    return stress_list


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
