import pygtrie
import spacy


class Concordance:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.trie = pygtrie.StringTrie()
        self.trie.enable_sorting()
        self.sent_map = {}
        self.max_word_len = 0

    def _item_prefix(self, idx):
        import string
        increment = int(idx / 26)
        offset = idx % 26
        letters = list(string.ascii_lowercase)
        letter = letters[offset]
        count = 0
        for values in self.trie.values():
            count += len(values)
        width = int(count / 26) + 3
        return '{}.'.format(letter.ljust(increment + 1, letter)).ljust(width)

    def output(self):
        idx = 0
        for key in self.trie.keys():
            for word in self.trie[key]:
                sent_idx = self.sent_map[word]
                line = '{}{} {{{}:{}}}'.format(
                    self._item_prefix(idx),
                    word.ljust(self.max_word_len+4),
                    len(sent_idx),
                    ','.join('{}'.format(i) for i in sent_idx))
                print(line)
                idx += 1

    def process_sentence(self, sentence, index):
        doc = self.nlp(sentence)
        for token in doc:
            # skip tokens that are solely punctuation or whitespace
            if token.is_punct or token.is_space:
                continue
            word = token.text

            if len(word) > self.max_word_len:
                self.max_word_len = len(word)

            # if a proper noun, store the word as-is, otherwise convert to lowercase
            word = word if token.pos_ == 'PROPN' else word.lower()

            if word.lower() in self.trie:
                if word not in self.trie[word.lower()]:
                    self.trie[word.lower()].append(word)
            else:
                self.trie[word.lower()] = [word]

            # add the sent index to the map
            if word in self.sent_map:
                self.sent_map[word].append(index)
            else:
                self.sent_map[word] = [index]

    def get_sentences(self, filename):
        with open(filename) as input_file:
            contents = input_file.read()
            doc = self.nlp(contents)
            return doc.sents


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate Concordance")
    parser.add_argument("--input", help="Text input file", required=True)
    args = parser.parse_args()

    concordance = Concordance()

    sentences = concordance.get_sentences(args.input)
    index = 1
    for sentence in sentences:
        concordance.process_sentence(sentence.text, index)
        index += 1

    concordance.output()


if __name__ == "__main__":
    main()
