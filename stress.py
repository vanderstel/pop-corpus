"""
Parses the CMU dictionary into a usable format.

Modified by Joseph VanderStel; based on work by Adam Waller and Ivan Tan.
"""

import string


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


def skip_comment_generator(file):
    """
    Returns a generator that skips the blank lines of a file,
    as well as several types of comments:
        - C-style:  /* */
        - CMU dict: ;
        - Corpus:   %
    """
    in_comment_block = False
    for line in file:
        if line[0] in ';%\n':
            continue
        elif '/*' in line:
            if '*/' not in line:
                in_comment_block = True
        elif '*/' in line:
            in_comment_block = False
        elif not in_comment_block:
            yield line


def format_word(word):
    """
    Remove spaces, line markers, punctuation and make uppercase.
    """
    return word \
        .rstrip() \
        .upper() \
        .translate(None, ',."!')


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
    return emphasis_dict


def modify_dict(dictionary):
    """
    Override entries in the CMU dictionary, and add new ones.
    (Mutate the data structure passed in.)
    """
    for entry in read_word_file(EXTENSION_FILENAME):
        dictionary[format_word(entry[0])] = entry[1:]
    return dictionary


dictionary = build_dict()
modify_dict(dictionary)
