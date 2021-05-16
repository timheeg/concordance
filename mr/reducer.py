#! python

import sys

current_word = None
current_sent_list = []
word = None

for line in sys.stdin:
    line.strip()
    word, sent_idx = line.split('\t', 1)

    try:
        sent_idx = int(sent_idx)
    except ValueError:
        continue

    if current_word == word:
        current_sent_list.append(sent_idx)
    else:
        if current_word:
            print("{}\t{}".format(current_word, ",".join(str(i) for i in current_sent_list)))
        current_sent_list = [sent_idx]
        current_word = word

if current_word == word:
    print("{}\t{}".format(current_word, ",".join(str(i) for i in current_sent_list)))
