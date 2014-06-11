from Tix import INTEGER
from _ctypes import Py_INCREF
import os
import pickle
import nltk

h_dict = pickle.load(open('corpus/cleaned_dict.pickle', 'rb'))

nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk'))

file_list = []

MAX_SEARCH_RANGE = 5


def rule_parser(tagged_data):
    parser = nltk.RegexpParser('''
        NP:   {<NN|NNS|NNP|NNPS|NE>}
        NPs:  {<NP> (<,|CC> <NP>)+}
    ''')

    return parser.parse(tagged_data)


def find_hypernyms(pre_parsed_data, hypernym_list):
    hypernym_positions = []

    for n in range(len(pre_parsed_data)):
        if isinstance(pre_parsed_data[n], nltk.tree.Tree):
            if pre_parsed_data[n].node == 'NP':
                if pre_parsed_data[n][0][0] in hypernym_list:
                    hypernym_positions.append((n, pre_parsed_data[n][0][0]))

    return hypernym_positions


def find_pattern(pre_parsed_data, hypernym, hypernym_list):
    left = []
    right = []
    start_pos = hypernym[0]

    def add_to_list(current_list, element, position, has_hyponym):
        try:
            if isinstance(element[position], nltk.tree.Tree):
                current_list.append((element[position][0][0], element[position].node))

                if element[position].node == 'NP':
                    if element[position][0][0] in hypernym_list[hypernym[1]]:
                        has_hyponym.append(len(current_list))

                elif element[position].node == 'NPs':
                    for possible_np in element[position]:
                        if isinstance(possible_np, nltk.tree.Tree):
                            if possible_np[0][0] in hypernym_list[hypernym[1]]:
                                has_hyponym.append(len(current_list))
            else:
                current_list.append((element[position][0], element[position][1]))
        except IndexError:
            pass

    # search the right side for a pattern
    has_hyponym = []
    for i in range(start_pos, start_pos + MAX_SEARCH_RANGE, 1):
        add_to_list(right, pre_parsed_data, i, has_hyponym)
    if has_hyponym:
        return 'right', right[:has_hyponym[-1]]

    has_hyponym = []
    # search the left side for a pattern
    for i in range(start_pos, start_pos - MAX_SEARCH_RANGE, -1):
        add_to_list(left, pre_parsed_data, i, has_hyponym)
    if has_hyponym:
        left.reverse()
        return 'left', left[(MAX_SEARCH_RANGE - has_hyponym[-1]):]

    return None


for root, subFolders, files in os.walk(os.path.join(os.path.dirname(__file__), 'corpus', 'tagged')):
    for current_file in files:
        if current_file.endswith(".pickle"):
            file_list.append(os.path.join(root, current_file))

for input_file in file_list:
    tagged_data = pickle.load(open(input_file, 'rb'))
    pre_parsed_data = rule_parser(tagged_data)

    hypernym_positions = find_hypernyms(pre_parsed_data, h_dict.keys())

    for hypernym in hypernym_positions:
        rule = find_pattern(pre_parsed_data, hypernym, h_dict)
        if rule:
            # TODO store the rules in a usable format and save them to a file with the iteration number
            print(rule)