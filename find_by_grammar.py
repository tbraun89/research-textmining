from multiprocessing import Process, JoinableQueue, Manager
import os
import sys
import pickle
import nltk


nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk'))


def search(output_dict, rules_file):
    rules = [rule.split(' | ') for rule in pickle.load(open(rules_file, 'rb'))]
    file_list = JoinableQueue()
    word_dict = Manager().dict()

    for root, subFolders, files in os.walk(os.path.join(os.path.dirname(__file__), 'corpus', 'tagged')):
        for current_file in files:
            if current_file.endswith(".pickle"):
                file_list.put(os.path.join(root, current_file))
                #break  # TODO remove (only for testing with one file)

    file_count = file_list.qsize()

    def worker():
        def rule_parser(tagged_data):
            parser = nltk.RegexpParser('''
                NP:   {<NN|NNS|NNP|NNPS|NE>}
                NPs:  {<NP> (<,|CC> <NP>)+}
            ''')

            return parser.parse(tagged_data)

        def get_nltk_word(data):
            if isinstance(data, nltk.tree.Tree):
                if isinstance(data[0], tuple):
                    return data[0][0]
                else:
                    return data[0]
            else:
                return data[0]

        def add_to_dict(hypernym, hyponym):
            if not hyponym in word_dict.keys():
                old_list = word_dict.get(hypernym)

                if not old_list:
                    old_list = [hyponym]
                else:
                    if not hyponym in old_list:
                        old_list.append(hyponym)

                word_dict[hypernym] = old_list

        def apply_rules(data, position):
            for rule in rules:
                # search right side
                if rule[0] == 'HYPERNYM':
                    possible_hypernym = get_nltk_word(data[position])
                    error = False
                    word_count = 1

                    for word in rule[1:-1]:
                        try:
                            if word != get_nltk_word(data[position + word_count]):
                                error = True

                            word_count += 1
                        except IndexError:
                            pass

                    try:
                        if not error:
                            if isinstance(data[position + word_count], nltk.tree.Tree):
                                if data[position + word_count].node == 'NP' and rule[-1] == 'NP':
                                    add_to_dict(possible_hypernym, data[position + word_count][0][0])
                                    break
                                elif data[position + word_count].node == 'NPs' and rule[-1] == 'NPs':
                                    for node in data[position + word_count]:
                                        if isinstance(node, nltk.tree.Tree):
                                            add_to_dict(possible_hypernym, node[0][0])
                                            break
                    except IndexError:
                        pass

                # search left side
                elif rule[-1] == 'HYPERNYM':
                    possible_hypernym = get_nltk_word(data[position])
                    error = False
                    word_count = -1
                    nrule = list(rule)
                    nrule.reverse()

                    for word in nrule[1:-1]:
                        try:
                            if word != get_nltk_word(data[position + word_count]):
                                error = False

                            word_count -= 1
                        except IndexError:
                            pass

                    try:
                        if not error:
                            if isinstance(data[position + word_count], nltk.tree.Tree):
                                if data[position + word_count].node == 'NP' and rule[-1] == 'NP':
                                    add_to_dict(possible_hypernym, data[position + word_count][0][0])
                                    break
                                elif data[position + word_count].node == 'NPs' and rule[-1] == 'NPs':
                                    for node in data[position + word_count]:
                                        if isinstance(node, nltk.tree.Tree):
                                            add_to_dict(possible_hypernym, node[0][0])
                                            break
                    except IndexError:
                        pass

        while not file_list.empty():
            input_file = file_list.get()

            tagged_data = rule_parser(pickle.load(open(input_file, 'rb')))

            for n in range(len(tagged_data)):
                if isinstance(tagged_data[n], nltk.tree.Tree):
                    if tagged_data[n].node == 'NP':
                        apply_rules(tagged_data, n)

            percentage = 100.0 - ((float(file_list.qsize()) / float(file_count)) * 100.0)
            sys.stdout.write("\rProgress: {0:.2f}%".format(percentage))
            sys.stdout.flush()

            file_list.task_done()

    sys.stdout.write("\rProgress: 0.00%")

    for pid in range(8):
        process = Process(target=worker, args=())
        process.daemon = True
        process.start()

    file_list.join()
    print('')

    pickle_dict = dict()

    for key in word_dict.keys():
        pickle_dict[key] = word_dict.get(key)

    pickle.dump(pickle_dict, open(output_dict, 'wb+'), 2)
