"""
Parses the CMU dictionary into a usable format.

Modified by Joseph VanderStel; based on work by Adam Waller and Ivan Tan.
"""

import string


CMU_FILENAME = 'dictionary/cmudict.txt'
FUNCTION_WORD_FILENAME = 'dictionary/function_words.txt'
NON_WORD_FILENAME = 'dictionary/non_words.txt'

def read_word_file(filename):
    """
    Return word list from file.
    """
    entries = []
    try:
        with open(filename, 'r') as file:
            for entry in file.readlines():
                if entry[0] != ';': # skip comments
                    entries.append(entry.split())
    except IOError:
        pass
    return entries


def format_word(word):
    """
    Remove spaces, line markers, punctuation and make uppercase.
    """
    return word \
        .rstrip() \
        .translate(string.maketrans("",""), string.punctuation) \
        .upper()


def build_dict():
    """
    Return data structure for pronunciation dictionary
    with relative emphasis levels.
    """
    emphasis_dict = {}
    for entry in read_word_file(CMU_FILENAME):
        word = entry[0].translate(string.maketrans("", ""), string.punctuation)
        emph_list = []
        for syl in entry[1:len(entry)]:
            try:
                emphlevel = int(syl[-1])
                emph_list.append(emphlevel)
            except ValueError:
                continue
        emphasis_dict[word] = emph_list
    return emphasis_dict


def modify_dict(dictionary):
    """
    Mutate the data structure passed in.
    """
    for word in read_word_file(FUNCTION_WORD_FILENAME):
        word = format_word(word)
        if word in dictionary and len(dictionary[word]) == 1:
            dictionary[word] = [0]

    for word in read_word_file(NON_WORD_FILENAME):
        dictionary[format_word(word)] = [3]
    return dictionary


dictionary = build_dict()
dictionary = modify_dict(dictionary)
