from collections import OrderedDict, Counter, defaultdict
from functools import partial
import os

import click

import analyze

@click.command()
def cli():
    """Analyze corpus files."""
    years, p, tempi = analyze.count_syncopations()
    analyze.get_all(years, analyze.SyncopationType.WEAK_FOURTH_POSITION)
    # analyze.subtype(years, analyze.SyncopationType.SECOND_POSITION, analyze.SyncopationType.DURATIONAL)
    # analyze.all_by_tempo(tempi, 20)

