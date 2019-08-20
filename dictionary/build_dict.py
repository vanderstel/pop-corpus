"""
Parses the CMU dictionary into a usable format.

(Based on work by Adam Waller & Ivan Tan.)
"""

import string

from utils import skip_comment_generator, format_word


CMU_FILENAME = 'dictionary/cmudict.txt'
EXTENSION_FILENAME = 'dictionary/extension.txt'

def read_word_file(filename):
    """
    Return word list from file.
    """
    entries = []
    try:
        with open(filename, 'r') as file:
            for entry in skip_comment_generator(file):
                entries.append(entry.split())
    except IOError:
        pass
    return entries


def modify_dict(dictionary):
    """
    Override entries in the CMU dictionary, and add new ones.
    (Mutate the data structure passed in.)
    """
    for entry in read_word_file(EXTENSION_FILENAME):
        dictionary[format_word(entry[0])] = entry[1:]
    return dictionary


def build_dict():
    """
    Return data structure for pronunciation dictionary
    with relative emphasis levels.
    """
    emphasis_dict = {}
    for entry in read_word_file(CMU_FILENAME):
        emph_list = []
        for syl in entry[1:len(entry)]:
            try:
                emphlevel = int(syl[-1])
                emph_list.append(emphlevel)
            except ValueError:
                continue
        emphasis_dict[entry[0]] = emph_list
    return modify_dict(emphasis_dict)

dictionary = build_dict()
