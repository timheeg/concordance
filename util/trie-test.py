

data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dictum velit in enim varius, " \
       "quis pretium metus efficitur. Aliquam nisi lacus, hendrerit non tortor ornare, dapibus varius " \
       "nisl. Quisque enim tellus, tincidunt non enim ac, blandit tristique massa. Pellentesque " \
       "tincidunt commodo suscipit."


def test_char():
    print('CharTrie Test')
    print('-------------')
    import pygtrie
    trie = pygtrie.CharTrie()
    trie.enable_sorting()
    for word in data.split():
        trie[word.lower()] = True
    print('K : ', ', '.join(trie.keys()))


def test_string():
    print('StringTrie Test')
    print('---------------')
    import pygtrie
    trie = pygtrie.StringTrie()
    trie.enable_sorting()
    for word in data.split():
        trie[word.lower()] = word
    print('K : ', ', '.join(trie.keys()))
    print('V : ', ', '.join(trie.values()))


def test():
    test_char()
    print('=========')
    test_string()


if __name__ == "__main__":
    test()
