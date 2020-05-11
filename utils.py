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
        if line[0] in '";%\n':
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
    out_str = word.rstrip().upper()
    unwanted_chars = ',."!'
    for char in unwanted_chars:
        out_str = out_str.replace(char, '')
    return out_str
