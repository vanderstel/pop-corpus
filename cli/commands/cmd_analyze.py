import os
from collections import OrderedDict, Counter, defaultdict

import click

YEAR_LIST_FILE = 'year_list.txt'
OUTPUT_DIRECTORY = 'output/'

years = OrderedDict()

@click.command()
def cli():
    """Analyze corpus files."""
    with open(YEAR_LIST_FILE, 'r') as file:
        for song in file.read().splitlines():
            try:
                year, name = song.strip().split(' ')
            except ValueError:
                pass
            counts = Counter()
            try:
                song_file = open(os.path.join(OUTPUT_DIRECTORY, name + '.txt'), 'r')
            except:
                print('{} in list doesn\'t exist in output directory'.format(name))
                continue

            # if year != '1913':
            #     continue

            song_events = song_file.read().splitlines()
            for i, event in enumerate(song_events):
                try:
                    onset, offset, _midi, _sd, stress, syllable = event.split(' ')
                except ValueError:
                    continue
                beat = onset.split('.')[1]
                # duration = float(offset) - float(onset)
                is_stressed = int(stress) == 1
                counts['total'] += 1

                if beat in ['125', '375', '625', '875']:
                    # Is weak 8th beat

                    # counts['offbeat_8th'] += 1
                    beat_size = 0.125

                    try:
                        next = song_events[i + 1]
                    except IndexError:
                        counts['positional'] += 1
                        break
                    try:
                        next_onset, _, _, _, next_stress, next_syllable = next.split(' ')
                    except ValueError:
                        continue
                    next_is_stressed = int(next_stress) == 1
                    if float(next_onset) > float(onset) + beat_size:
                        counts['positional'] += 1
                        if is_stressed:
                            counts['anticipatory'] += 1
                        if beat in ['125', '625']:
                            counts['2nd_position'] += 1
                        else:
                            counts['4th_position'] += 1
                    elif float(next_onset) == (float(onset) + beat_size):
                    # elif (float(onset) + beat_size - 0.005) < float(next_onset) < (float(onset) + beat_size + 0.005):  # CHANGED
                        if is_stressed and not next_is_stressed:
                            counts['lexical'] += 1
                            print('8th lexical:', syllable, next_syllable)

                # Identical, but 16th (make DRY'er)
                if beat in ['062', '188', '312', '438', '562', '688', '812', '938']:
                    # Is weak 16th beat

                    # counts['offbeat_16th'] += 1
                    beat_size = 0.062

                    try:
                        next = song_events[i + 1]
                    except IndexError:
                        counts['positional_16th'] += 1
                        break
                    try:
                        next_onset, _, _, _, next_stress, next_syllable = next.split(' ')
                    except ValueError:
                        continue
                    next_is_stressed = int(next_stress) == 1
                    next_position = (float(onset) + beat_size)
                    # print(float(next_onset), next_position + 0.002)
                    if float(next_onset) > next_position + 0.002:
                        counts['positional_16th'] += 1
                        if is_stressed:
                            counts['anticipatory_16th'] += 1
                        if beat in ['062', '312', '562', '812']:
                            counts['2nd_position_16th'] += 1
                        else:
                            counts['4th_position_16th'] += 1
                    # Give some slack
                    # elif float(next_onset) == next_position:
                    elif (next_position - 0.002) < float(next_onset) < (next_position + 0.002):
                        if is_stressed and not next_is_stressed:
                            counts['lexical_16th'] += 1
                            print('16th lexical:', syllable, next_syllable)

            years[int(year)] = counts
