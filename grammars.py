from multiprocessing import Process, JoinableQueue, Manager
import os
import pickle
import nltk
import sys


nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk'))

MAX_SEARCH_RANGE = 5
THRESHOLD = 2

WORD_BLACKLIST = [
    'yeah',
    'oh',
    'uh-huh',
    '.',
    'um-hum',
    'um',
    'uh',
    'huh',
    '(',
    ')',
    'hm',
    'wow'
]


def learning(input_dict, output_rules):
    def worker():
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

        def add_rule(rule):
            if len(rule[1]) >= 3:
                rts = []

                count = 0
                for element in rule[1]:
                    if element[1] == 'NPs' or element[1] == 'NP':
                        if count == 0 or count == len(rule[1]) - 1:
                            rts.append(element[1])
                        else:
                            if element[1] == 'NP':
                                rts.append(element[0])
                            else:
                                for node in element[1]:
                                    rts.append(node[0])
                    else:
                        rts.append(element[0])

                    count += 1

                if rule[0] == 'left':
                    rts[len(rule[1]) - 1] = 'HYPERNYM'
                else:
                    rts[0] = 'HYPERNYM'

                rts_str = ' | '.join(rts)

                if rts_str in rules:
                    rules[rts_str] += 1
                else:
                    rules[rts_str] = 1

        while not file_list.empty():
            input_file = file_list.get()

            tagged_data = pickle.load(open(input_file, 'rb'))

            pre_parsed_data = rule_parser(tagged_data)

            hypernym_positions = find_hypernyms(pre_parsed_data, h_dict.keys())

            for hypernym in hypernym_positions:
                rule = find_pattern(pre_parsed_data, hypernym, h_dict)

                if rule:
                    add_rule(rule)

            percentage = 100.0 - ((float(file_list.qsize()) / float(file_count)) * 100.0)
            sys.stdout.write("\rProgress: {0:.2f}%".format(percentage))
            sys.stdout.flush()

            file_list.task_done()

    def blacklist_filter(rule):
        result = True

        for word in WORD_BLACKLIST:
            if word in rule:
                result = False

        return result

    h_dict = pickle.load(open(input_dict, 'rb'))

    rules = Manager().dict()
    file_list = JoinableQueue()
    sys.stdout.write("\rProgress: 0.00%")

    for root, subFolders, files in os.walk(os.path.join(os.path.dirname(__file__), 'corpus', 'tagged')):
        for current_file in files:
            if current_file.endswith(".pickle"):
                file_list.put(os.path.join(root, current_file))

    file_count = file_list.qsize()

    for pid in range(8):
        process = Process(target=worker, args=())
        process.daemon = True
        process.start()

    file_list.join()
    print('')

    # filter the rules and save them
    filtered_rules = {k: v for k, v in rules.items() if v >= THRESHOLD and blacklist_filter(k)}
    rule_list = sorted(filtered_rules.keys(), key=filtered_rules.get)
    rule_list.reverse()

    pickle.dump(rule_list, open(output_rules, 'wb+'), 2)
