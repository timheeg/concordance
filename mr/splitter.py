#! python

import spacy
import sys

nlp = spacy.load("en_core_web_sm")

text = ""
max_batch_size = 20  # number of lines per batch
batch_size = 0
sent_count = 0

for line in sys.stdin:
    line = line.strip()

    # skip empty lines
    if line == '':
        continue

    text += line + '\n'
    batch_size += 1
    if batch_size <= max_batch_size:
        continue

    # process batch
    doc = nlp(text)
    sentences = doc.sents
    # output all identified sentences except the last one
    sent_list = list(sentences)
    for s in sent_list[:-1]:
        s = s.text.strip().replace('\n', ' ').replace('\r', ' ')
        if s != '':
            sent_count += 1
            print("{}\t{}".format(sent_count, s))

    # save the last sentence into the buffer to process with the next batch
    text = sent_list[-1:][0].text.strip() + '\n'

    batch_size = 1  # reset batch

# process final data once input stops
doc = nlp(text)
sentences = doc.sents
for s in sentences:
    s = s.text.strip().replace('\n', ' ').replace('\r', ' ')
    if s != '':
        sent_count += 1
        print("{}\t{}".format(sent_count, s))
