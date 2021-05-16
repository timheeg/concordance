#! python

import spacy
import sys

nlp = spacy.load("en_core_web_sm")

for line in sys.stdin:
    line = line.strip()
    sentence_idx, sentence = line.split('\t', 1)

    doc = nlp(sentence)
    for token in doc:
        # skip tokens that are solely punctuation or whitespace
        if token.is_punct or token.is_space:
            continue
        word = token.text

        # if a proper noun, store the word as-is, otherwise convert to lowercase
        word = word if token.pos_ == 'PROPN' else word.lower()

        print("{}\t{}".format(word, sentence_idx))
