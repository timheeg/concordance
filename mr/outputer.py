#! python

import sys

num_words = 0
max_word_len = 0
count = 0
lines = []


def _item_prefix(idx):
    import string
    increment = int(idx / 26)
    offset = idx % 26
    letters = list(string.ascii_lowercase)
    letter = letters[offset]
    width = int(num_words / 26) + 3
    return '{}.'.format(letter.ljust(increment + 1, letter)).ljust(width)


for line in sys.stdin:
    lines.append(line.strip())

    word, sent_idx_list = line.split('\t', 1)
    num_words += 1
    if len(word) > max_word_len:
        max_word_len = len(word)


# post processing
for line in lines:
    word, sent_idx_list = line.split('\t', 1)

    sidx = sent_idx_list.strip().split(',')

    line = '{}{} {{{}:{}}}'.format(
        _item_prefix(count),
        word.ljust(max_word_len + 4),
        len(sidx),
        ','.join('{}'.format(i) for i in sidx))
    print(line)
    count += 1
