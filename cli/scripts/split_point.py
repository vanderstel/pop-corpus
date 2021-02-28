#!/usr/bin/python
#
# Originally written by Davy Temperley in Perl.
#

import math
from pathlib import Path
import sys
from typing import List, Optional, Tuple


try:
    file = Path(sys.argv[1])
except IndexError:
    print('Filename should be only arg')
    sys.exit(1)

if not file.is_file():
    raise FileNotFoundError

vals = []
with file.open() as f:
    for line in f:
        val = line.strip('\n')
        try:
            vals.append(float(val))
        except ValueError:
            print(f'{val} is not a float')
            sys.exit(1)


CUSHION = 1

best_dev_sum = float('inf')
best_dev_split_point: Optional[int] = None
best_mean1: Optional[int] = None
best_mean2: Optional[int] = None


def sum_sq_dev(li: List[int]) -> Tuple[int, int]:
    avg = sum(li) / len(li)
    dev = 0
    for v in li:
        dev += (v - avg) ** 2
    return dev, avg


for i in range(CUSHION, len(vals) - CUSHION):
    first_half = vals[:i + 1]
    second_half = vals[i + 1:]

    dev1, avg1 = sum_sq_dev(first_half)
    dev2, avg2 = sum_sq_dev(second_half)
    dev_sum = dev1 + dev2

    if dev_sum < best_dev_sum:
        best_dev_sum = dev_sum
        best_dev_split_point = i
        best_mean1 = avg1
        best_mean2 = avg2


print(f'''
    Min summed squared deviations = {best_dev_sum:.2f}
    Split point = {best_dev_split_point}
    Mean1 = {best_mean1:.2f}
    Mean2 = {best_mean2:.2f}
''')
