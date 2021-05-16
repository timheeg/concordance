# Concordance: Brute Force Approach

Parse for sentences:
- if a sentence delimiter is not found, append line to sentence
- otherwise split
    - append the 1st part to sentence,
    - add sentence to list,
    - clear local sentence to continue
    - re-process 2nd part for sentence delim

For each sentence, tokenize into words.

For each word (i.e. token),
- add word to trie (for alpha sorting)
- add word and sentence index to map, where
    - key = word,
    - value = list of sentence indexes

Iterate through the trie using depth-first search in order to 
output words alphabetically.

Use the trie words as key lookups in the map to retrieve the
corresponding sentence index list.


## Defining a Sentence

It only took a few minutes of thinking about how to define a sentence
delimiter to realize there are a plethora of problems to handle in the
English language, such as:

* multiple end punctuation, e.g. "first!?!!??! Second"
* abbreviations, e.g. "e.g. example, viz. namely"
* no space after punctuation, e.g. "first.Second"
* whitespace before punctuation, e.g. "first . Second"
* non-capitalized first word in sentence, e.g. "first. second"

It only took a few minutes of thinking about how trying to define a
robust sentence delimiter is complex to think of Natural Language
Processing (NLP). I haven't utilized that since Wright State several
years ago, but encountered it in several courses.

I googled python natural language processing and quickly found
spaCy https://spacy.io/.

I installed spacy and its English support.
```
(concordance) pip install spacy
(concordance) python -m spacy download en_core_web_sm
```

## Python Trie

I don't know of any specify python trie library, so I had to google it.

I spent to much time investigating various python trie solutions until
I found google's pygtrie python library.

The sorting provided by pygtrie is ascii-based so A-Z comes sorted before
a-z. So rudimentary sorting of the individual word is insufficient.

## Order of Proper Nouns

Words in the concordance are sorted case insensitive.

Each word is converted to lower case, ignoring whether it is capitalized
as the start of a sentence. Proper nouns are not converted to lower case.

I can use NLP to determine whether a word (token) is a proper noun,
thereby retaining its capitalization.

However, the problem is that the Trie sorting is ascii based, such that
A-Z are ordered before a-z. So all words must be converted to lowercase
regardless of their part-of-speech when adding them to the trie; however,
the case-correct words can be stored as values in a StringTrie.

See `util/trie-test.py` for an example demonstrating the CharTrie
is insufficient to deal with the ordering of proper nouns, and the
StringTrie solves this iterating over values when storing keys as lowercase
and original case as values. 

```
(concordance) > python trie-test.py
CharTrie Test
-------------
K :  ac,, adipiscing, aliquam, amet,, blandit, commodo, consectetur, dapibus, dictum, dolor, efficitur., elit., enim, hendrerit, in, ipsum, lacus,, lorem, massa., metus, nisi, nisl., non, ornare,, pellentesque, pretium, quis, quisque, sed, sit, suscipit., tellus,, tincidunt, tortor, tristique, varius, varius,, velit
=========
StringTrie Test
---------------
K :  ac,, adipiscing, aliquam, amet,, blandit, commodo, consectetur, dapibus, dictum, dolor, efficitur., elit., enim, hendrerit, in, ipsum, lacus,, lorem, massa., metus, nisi, nisl., non, ornare,, pellentesque, pretium, quis, quisque, sed, sit, suscipit., tellus,, tincidunt, tortor, tristique, varius, varius,, velit
V :  ac,, adipiscing, Aliquam, amet,, blandit, commodo, consectetur, dapibus, dictum, dolor, efficitur., elit., enim, hendrerit, in, ipsum, lacus,, Lorem, massa., metus, nisi, nisl., non, ornare,, Pellentesque, pretium, quis, Quisque, Sed, sit, suscipit., tellus,, tincidunt, tortor, tristique, varius, varius,, velit
```

## Abbreviations

The problem example solution shows the word "i.e." in the concordance.

spaCy already defines several forms of "i.e." as tokenizer
exceptions for the english language. This works for abbreviations
like "i.e" or "e.g.". See
https://github.com/explosion/spaCy/blob/master/spacy/lang/en/tokenizer_exceptions.py#L493


## Concordance Item Prefix

The problem example solution shows an ordered item list prefix using lowercase
letters. After 26 letters, it then shows double lowercase letters.

For this solution, I am assuming that the list item format is single
letters, double letters, triple letters, etc.
  
The problem example solution shows the ordered item list prefix left justified
with a width of the widest prefix plus 1 space.

For this solution, calculate the longest prefix based on the total number
of words in the concordance. Left justify with a width of the widest prefix
plus 1 space.


## Running

Active the virtual environment.
```
> source <env>/concordance/Scripts/activate
```

Run the concordance with an input file.
```
(concordance) > python concordance.py --input ..\res\example.txt
```

Save concordance output.
```
(concordance) > python concordance.py --input ..\res\example.txt >
    output\example.concordance.txt
```


## Examples

The `/res` folder contains a couple examples.

* `example.txt` is the text provided in the problem statement.
* `20k.txt` is approx. 20k words of random "Lorem ipsum" text.
* `turing.txt` is a rudimentary copy of Alan Turing's "Turing Test" paper.

The `/output` folder contains the results of the concordance
run against those example inputs.


## References

Here are the various sites I visited in support of this effort.

Python argparse
https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_argument

spaCy https://spacy.io/

scaCy api https://spacy.io/api

spaCy linguistic features https://spacy.io/usage/linguistic-features

Google pygtrie https://github.com/google/pygtrie

SO: Python join a list of integers
https://stackoverflow.com/questions/11139330/python-join-a-list-of-integers

Real Python: A Guide to the Newer Python String Format Techniques
https://realpython.com/python-formatted-output

SO: alphabet range in python
https://stackoverflow.com/questions/16060899/alphabet-range-in-python
