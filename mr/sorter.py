#! python

import pygtrie
import sys

trie = pygtrie.StringTrie()
trie.enable_sorting()
lines = {}

for line in sys.stdin:
    line = line.strip()
    word, sent_idx = line.split('\t', 1)

    if word.lower() in trie:
        if word not in trie[word.lower()]:
            trie[word.lower()].append(word)
    else:
        trie[word.lower()] = [word]

    if word in lines:
        lines[word].append(line)
    else:
        lines[word] = [line]

for key in trie.keys():
    for word in trie[key]:
        for line in lines[word]:
            print("{}".format(line))
