import json
import os

trie = {}
sentences = {}


def read_data_from_file(file_name):
    the_file = open(file_name)
    return the_file.read().split("\n")


def add_sentence_to_data(sentence, index, source):
    sentences[index] = {"sentence": sentence, "source": source}


def add_sub_to_trie(sub, id_, offset):
    tmp_trie = trie
    for letter in sub:
        if letter not in tmp_trie.keys():
            tmp_trie[letter] = {}
            tmp_trie[letter]['sentences_ids'] = {id_: {'offset': offset}}
        elif id_ not in tmp_trie[letter]['sentences_ids']:
            tmp_trie[letter]['sentences_ids'][id_] = {'offset': offset}
        tmp_trie = tmp_trie[letter]


def add_sentence_to_trie(sentence, id_):
    for index in range(len(sentence)+1):
        add_sub_to_trie(sentence[index:], id_, index)


def read_directory_data(dir_):
    count_file = 0
    directory = os.path.normpath(dir_)
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            file_ = open(os.path.join(subdir, file), encoding="utf8")
            for sentence in file_:
                add_sentence_to_trie(sentence.lower(), count_file)
                add_sentence_to_data(sentence, count_file, str(file))
                count_file += 1
            file_.close()


def init_data():
    directory = "C:/Users/RENT/Desktop/לימודים/data_files"
    read_directory_data(directory)
    data_to_json = {"sentences": sentences, "trie": trie}
    with open("data.json", "w") as the_file:
        json.dump(data_to_json, the_file)


init_data()
