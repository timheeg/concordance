
def get_reduced_content(filename):
    with open(filename) as input_file:
        text = ''
        for line in input_file.readlines():
            if line.strip() == '':
                continue
            text += line.strip().replace('\n', ' ').replace('\r', ' ') + '\n'
        return text


def output_reduced_content(file_prefix, text):
    filename = "output/{}.reduced.txt".format(file_prefix)
    with open(filename, 'w') as file:
        file.write(text)


def output_sentences(file_prefix, sentences):
    filename = "output/{}.sentences.txt".format(file_prefix)
    with open(filename, 'w') as file:
        idx = 1
        for s in sentences:
            s = s.text.strip().replace('\n', ' ').replace('\r', ' ')
            file.write("{}\t{}\n".format(idx, s))
            idx += 1


def reduce_sentences(sentences):
    # remove all empty sentences
    return list(filter(lambda s: s.text.strip() != '', sentences))


def get_filename_(filename):
    import os.path
    return os.path.split(os.path.splitext(filename)[0])[1]
