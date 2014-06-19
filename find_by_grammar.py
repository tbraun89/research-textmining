from multiprocessing import Process, JoinableQueue
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
            if isinstance(data[0], nltk.Tree):
                return data[0][0][0]
            else:
                return data[0]

        def add_to_dict(hypernym, hyponym):
            old_list = word_dict.get(hypernym)

            if not old_list:
                old_list = [hyponym]

            word_dict[hypernym] = old_list

        def apply_rules(data, position):
            for rule in rules:
                # search right side # FIXME why does this find nothing? oO
                if rule[0] == 'HYPERNYM':
                    posible_hypernym = get_nltk_word(data[position])
                    error = False
                    posible_hyponym = None
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
                            if isinstance(data[position + word_count], nltk.Tree):
                                if data[position + word_count][1][1] == 'NP':
                                    print get_nltk_word(data[position + word_count])
                                    add_to_dict(posible_hypernym[0], get_nltk_word(data[position + word_count]))
                    except IndexError:
                        pass

                # search left side
                else:
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

    print word_dict
    # TODO save new dict


# TODO only for testing this should be called from learning.py
output_dict = input_dict = os.path.join(os.path.dirname(__file__), 'learning/dict-test.pickle')
output_rules = os.path.join(os.path.dirname(__file__), 'learning/rules-0.pickle')
search(output_dict, output_rules)