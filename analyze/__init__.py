from collections import (
    Counter,
    defaultdict,
    OrderedDict,
)
from dataclasses import dataclass
from enum import Enum
from functools import partial
import math
import os
from typing import (
    Counter as CounterType,
    Dict,
    List,
    Optional,
    Tuple,
)


YEAR_LIST_FILE = 'year_list.txt'
TEMPO_LIST_FILE = 'tempo_list.txt'
OUTPUT_DIRECTORY = 'output/'

QUARTER_BEAT_SIZE = 0.250
EIGHTH_BEAT_SIZE = 0.125
SIXTEENTH_BEAT_SIZE = 0.062


class SyncopationType(Enum):
    SECOND_POSITION = '2nd_position'
    FOURTH_POSITION = '4th_position'

    STRONG_FOURTH_POSITION = 'strong_4th_position'
    WEAK_FOURTH_POSITION = 'weak_4th_position'

    POSITIONAL = 'positional'
    ANTICIPATORY = 'anticipatory'
    LEXICAL = 'lexical'
    ONE_WORD_LEXICAL = 'one_word_lexical'
    DURATIONAL = 'durational'

    PRECEDED = 'preceded'
    UNPRECEDED = 'unpreceded'


class SyncopationSize(Enum):
    SIXTEENTH = 'sixteenth'
    EIGHTH = 'eighth'
    QUARTER = 'quarter'


class Event:
    def __init__(self, onset, offset, midi, sd, stress, syllable):
        self.beat = onset.split('.')[1]
        self.onset = float(onset)
        self.offset = float(offset)
        self.midi = int(midi)
        self.sd = int(sd)
        self.stress = int(stress)
        self.syllable = syllable

    @property
    def duration(self):
        return self.offset - self.onset

    @property
    def is_stressed(self):
        return self.stress == 1

    @property
    def is_weak_quarter(self):
        return self.beat in ['250', '750']

    @property
    def is_weak_eighth(self):
        return self.beat in ['125', '375', '625', '875']

    @property
    def is_weak_sixteenth(self):
        return self.beat in ['062', '188', '312', '438', '562', '688', '812', '938']

    @property
    def is_first_syllable(self):
        return self.syllable[-2] == '1'

    @property
    def is_fourth_position(self):
        is_4p = self.beat in (
            '375', '875',  # 8th level
            '188', '438', '688', '938',  # 16th level
        )
        return is_4p

    @property
    def is_strong_fourth_position(self):
        is_strong_4p = self.beat in (
            '875',  # 8th level
            '438', '938',  # 16th level
        )
        return is_strong_4p

    @property
    def is_weak(self):
        return (
            self.is_weak_eighth
            or self.is_weak_sixteenth
            or self.is_weak_quarter
        )

    @property
    def size(self) -> Optional[SyncopationSize]:
        if self.is_weak_quarter:
            return SyncopationSize.QUARTER
        elif self.is_weak_eighth:
            return SyncopationSize.EIGHTH
        elif self.is_weak_sixteenth:
            return SyncopationSize.SIXTEENTH
        return None


# Types hints
CountsByYear = Dict[str, CounterType]
CountsByTempo = Dict[str, CounterType]
SyncopationTypePercents = Dict[SyncopationType, List[float]]


def get_tempi():
    file = open(TEMPO_LIST_FILE, 'r')
    tempi_by_year = {}
    for line in file.read().splitlines():
        vals = line.strip().split(',')
        year = vals[0]
        tempo = vals[6]
        tempi_by_year[year] = tempo

    return tempi_by_year


tempi_by_year = get_tempi()


def count_syncopations() -> Tuple[CountsByYear, CountsByTempo, SyncopationTypePercents]:
    # Organizes data by year
    years = {}

    # Organizes data by onset in song
    intra_song_counts = defaultdict(list)

    # Organizes data by tempo
    tempi = defaultdict(Counter)

    # unique_lexical_syl = set()
    # lexical_non_pos_midi = set()
    file = open(YEAR_LIST_FILE, 'r')
    for song in file.read().splitlines():
        try:
            year, name = song.strip().split(' ')
        except ValueError:
            print('Year list file is not formatted correctly.')
            continue

        tempo = tempi_by_year[year]

        try:
            filename = f'{name}.txt'
            song_file = open(os.path.join(OUTPUT_DIRECTORY, filename), 'r')
        except Exception:
            print(f'{name} in list does not exist in output directory.')
            continue

        def _base_increment(
            key: str,
            c: CounterType = None,
            size: SyncopationSize = None,
            percentage_through_century: float = None,
        ):
            if percentage_through_century is not None:
                intra_song_counts[key].append(percentage_through_century)

            key = f'{key}_{size}'

            tempi[tempo][key] += 1

            c[key] += 1

        counts = Counter()
        song_events = song_file.read().splitlines()

        for i, event_str in enumerate(song_events):
            try:
                event = Event(*event_str.split(' '))
            except (ValueError, TypeError):
                # NOTE: Joy To The World output has a problem (reason for the TypeError)
                continue

            counts['total'] += 1

            if not event.is_weak:
                continue

            percentage_through_century = float(i) / float(len(song_events) - 1)
            increment = partial(
                _base_increment,
                c=counts,
                size=event.size,
                percentage_through_century=percentage_through_century,
            )

            increment('total')

            try:
                next_event_str = song_events[i + 1]
            except IndexError:
                increment(SyncopationType.POSITIONAL)
                break
            try:
                next_event = Event(*next_event_str.split(' '))
            except (ValueError, TypeError):
                continue

            beat_size: float
            if event.is_weak_quarter:
                beat_size = QUARTER_BEAT_SIZE
            elif event.is_weak_eighth:
                beat_size = EIGHTH_BEAT_SIZE
            else:
                beat_size = SIXTEENTH_BEAT_SIZE

            slack = 0.0 if not event.is_weak_sixteenth else 0.002
            next_position = event.onset + beat_size

            next_event_is_at_next_beat = False

            if event.is_weak_sixteenth and (next_position - slack) < next_event.onset < (next_position + slack):
                next_event_is_at_next_beat = True

            elif next_event.onset == next_position:
                # It's quarter or eighth
                # PAST FOR EIGHTH: elif (event.onset + beat_size - 0.005) < next_event.onset < (event.onset + beat_size + 0.005):  # CHANGED

                next_event_is_at_next_beat = True

            is_positional_syncopation = (next_event.onset > next_position + slack)

            if is_positional_syncopation:
                positional_type: SyncopationType
                if event.is_fourth_position:
                    positional_type = SyncopationType.FOURTH_POSITION
                    if event.is_strong_fourth_position:
                        increment(SyncopationType.STRONG_FOURTH_POSITION)
                    else:
                        increment(SyncopationType.WEAK_FOURTH_POSITION)

                else:
                    positional_type = SyncopationType.SECOND_POSITION

                increment(SyncopationType.POSITIONAL)
                increment(positional_type)

                if i > 0:
                    previous_event_str = song_events[i - 1]
                    previous_event = Event(*previous_event_str.split(' '))

                    if previous_event.onset + beat_size == event.onset:
                        increment(SyncopationType.PRECEDED)
                    else:
                        increment(SyncopationType.UNPRECEDED)

                if event.is_stressed:
                    increment(SyncopationType.ANTICIPATORY)

                if event.duration > beat_size:
                    increment(f'{positional_type}_{SyncopationType.DURATIONAL}')

                if event.is_stressed:
                    increment(f'{positional_type}_{SyncopationType.LEXICAL}')
                    if event.duration > beat_size:
                        increment(f'{positional_type}_{SyncopationType.LEXICAL}_{SyncopationType.DURATIONAL}')
            elif next_event_is_at_next_beat:
                if event.is_stressed and not next_event.is_stressed:
                    increment(SyncopationType.LEXICAL)
                    if not next_event.is_first_syllable:
                        # lexical_non_pos_midi.add((event.midi, next_event.midi))
                        # unique_lexical_syl.add((year, event.syllable, next_event.syllable))
                        increment(SyncopationType.ONE_WORD_LEXICAL)

        years[int(year)] = counts

    file.close()

    return years, tempi, intra_song_counts


def get_val(key: str, data) -> Tuple[float, float, float]:
    quarter = 0.0
    eighth = 0.0
    sixteenth = 0.0

    quarter_key = f'{key}_{SyncopationSize.QUARTER}'
    eighth_key = f'{key}_{SyncopationSize.EIGHTH}'
    sixteenth_key = f'{key}_{SyncopationSize.SIXTEENTH}'

    if quarter_key in data:
        quarter = float(data[quarter_key])

    if eighth_key in data:
        eighth = float(data[eighth_key])

    if sixteenth_key in data:
        sixteenth = float(data[sixteenth_key])

    return quarter, eighth, sixteenth


def totals(years: CountsByYear):
    quarter_total = 0
    eighth_total = 0
    sixteenth_total = 0

    for year, data in years.items():
        quarter, eighth, sixteenth = get_val(SyncopationType.POSITIONAL, data)
        quarter_total += quarter
        eighth_total += eighth
        sixteenth_total += sixteenth

    print(f'Quarter total: {quarter_total}')
    print(f'Eighth total: {eighth_total}')
    print(f'Sixteenth total: {sixteenth_total}')


def get_all(years: CountsByYear, sync_type: SyncopationType):
    with open('results/results.txt', 'w') as output_file:
        # output_file.write('Year, Score\n')  # 8th & 16th, over all events
        for year, data in years.items():
            _quarter, eighth, sixteenth = get_val(sync_type, data)
            val = eighth + sixteenth
            quotient = val / float(data['total'])
            print(year, quotient)
            output_file.write(f'{quotient}\n')


def all_by_tempo(tempi, base=None):
    '''
    For each unique tempo in the corpus, split up syncopations by
    SyncopationSize. Order by tempo.

    Optionally group tempi for larger bins.

    If base=20, group vals by 0-20bpm, 20-40bpm, 40-60bpm, etc.
    '''
    tempo_vals = [float(k) for k in tempi.keys() if k]
    tempo_vals.sort()

    output = defaultdict(Counter)

    def _round(x, b):
        return b * int(x/b)

    with open('results/results.txt', 'w') as output_file:
        output_file.write('Tempo, Quarter, Eighth, Sixteenth\n')  # 8th & 16th, over all events
        for tempo in tempo_vals:
            data = tempi[str(tempo)]

            quarter, eighth, sixteenth = get_val('total', data)
            # quarter, eighth, sixteenth = get_val(SyncopationType.POSITIONAL, data)
            tot = quarter + eighth + sixteenth
            if tot == 0:
                continue

            quarter_quotient = quarter / float(tot)
            eighth_quotient = eighth / float(tot)
            sixteenth_quotient = sixteenth / float(tot)

            if not base:
                output_file.write(f'{tempo}, {quarter_quotient}, {eighth_quotient}, {sixteenth_quotient}\n')
                continue

            counter = output[_round(tempo, base)]

            counter['quarter'] += quarter
            counter['eighth'] += eighth
            counter['sixteenth'] += sixteenth
            counter['tot'] += tot

        if base:
            for tempo, counter in output.items():
                print(tempo, counter)
                tot = counter['tot']

                if tot == 0:
                    continue

                quarter_quotient = counter['quarter'] / float(tot)
                eighth_quotient = counter['eighth'] / float(tot)
                sixteenth_quotient = counter['sixteenth'] / float(tot)

                output_file.write(f'{tempo}, {quarter_quotient}, {eighth_quotient}, {sixteenth_quotient}\n')


# Trash me
def syncopation_quotients_by_year_with_quarters(years: CountsByYear, sync_type: SyncopationType):
    with open('results/results.txt', 'w') as output_file:
        output_file.write('Year, Quarter, Eight, Sixteenth\n')  # 8th & 16th, over all events
        for year, data in years.items():
            quarter, eighth, sixteenth = get_val(sync_type, data)

            # print(float(data['total']))
            quarter_quotient = quarter / float(data['total'])
            eighth_quotient = eighth / float(data['total'])
            sixteenth_quotient = sixteenth / float(data['total'])

            output_file.write(f'{year}, {quarter_quotient}, {eighth_quotient}, {sixteenth_quotient}\n')


def percentages(
    sync_percents: SyncopationTypePercents,
    sync_type: SyncopationType,
):
    '''
    Intra-song change!
    '''
    slots = Counter()
    #
    # total = sum(p[sync])
    # percents = map(lambda i: i / total, p[sync])
    # print(percents)

    amount = 100
    for percents in sync_percents[sync_type]:
        rounded = math.floor(percents * amount) / amount
        # rounded = round(x, 1)
        slots[rounded] += 1

    # print(sum(p[sync]) / len(p[sync]))

    with open('results/results.txt', 'w') as output_file:
        output_file.write('Year, Score\n')

        keys = list(slots.keys())
        keys.sort()

        for k in keys:
            output_file.write(f'{k}, {slots[k]}\n')


def subtype(years: CountsByYear, sync, sub_sync):
    '''
    Percentage of sync that are also sub_sync
    '''
    key = f'{sync}_{sub_sync}'

    with open('results/results.txt', 'w') as output_file:
        output_file.write(f'{key}\n')
        total_subtype = 0
        total_type = 0

        for year, data in years.items():
            _quarter, eighth, sixteenth = get_val(sync, data)
            # Could keep these split to compare 8th and 16th
            val = eighth + sixteenth
            total_type += val


            _subtype_quarter, subtype_eighth, subtype_sixteenth = get_val(key, data)
            subtype_val = subtype_eighth + subtype_sixteenth
            total_subtype += subtype_val

        percentage = total_subtype / total_type
        output_file.write(f'{percentage}\n')


def reduce(years: CountsByYear, sync_type: SyncopationType):
    # Quarters  # could also be decades ...
    quarters = defaultdict(list)

    for year, data in years.items():
        _quarter, eighth, sixteenth = get_val(sync_type, data)
        val = eighth + sixteenth

        quotient = val / float(data['total'])
        quarters[year / 25].append(quotient)

    with open('results/results.txt', 'w') as output_file:
        output_file.write('Year, Score\n')  # 8th & 16th, over all events

        keys = quarters.keys()
        keys.sort()

        for k in keys:
            v = quarters[k]
            num = len(v)
            tot = 0
            for val in v:
                tot += val

            quarter_ave = tot / num

            output_file.write(f'{k*10}, {quarter_ave}\n')


def ratio(
    years: CountsByYear,
    numerator: SyncopationType,
    denominator: SyncopationType,
):
    # Compare two different syncopation types directly
    # E.g., 2nd / 4th ratio
    with open('results/results.txt', 'w') as output_file:
        output_file.write('Year, Score\n')
        for year, data in years.items():
            _quarter, eight, sixteenth = get_val(numerator, data)
            numerator_val = eighth + sixteenth

            _quarter, eight, sixteenth = get_val(denominator, data)
            denominator_val = eighth + sixteenth

            quotient = 0
            if float(denominator_val) == 0:
                if float(numerator_val) == 0:
                    quotient = 1
                else:
                    continue
            else:
                quotient = float(numerator_val) / float(denominator_val)

            output_file.write(f'{year}, {quotient}\n')
