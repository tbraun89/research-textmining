from multiprocessing import Process, JoinableQueue
import os
import sys
import pickle
import nltk


nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk'))


def search(output_dict, rules_file):
    rules = [rule.split(' | ') for rule in pickle.load(open(rules_file, 'rb'))]
    file_list = JoinableQueue()

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
            if isinstance(data[0], str):
                return data[0]
            else:
                return data[0][0][0]

        def apply_rules(data, position):
            for rule in rules:
                # search right side # FIXME why does this find nothing? oO
                if rule[0] == 'HYPERNYM':
                    possible_hypernym = get_nltk_word(data[position])
                    error = False
                    possible_hyponym = None
                    word_count = 1

                    for word in rule[1:]:
                        try:
                            if word != get_nltk_word(data[position + word_count]):
                                error = True
                            elif word == 'HYPONYM':
                                possible_hyponym = data[position + word_count]

                            word_count += 1
                        except IndexError:
                            pass

                    if possible_hyponym and not error:
                        print possible_hypernym + ' ~> ' + possible_hyponym

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

    # TODO save new dict


# TODO only for testing this should be called from learning.py
output_dict = input_dict = os.path.join(os.path.dirname(__file__), 'learning/dict-test.pickle')
output_rules = os.path.join(os.path.dirname(__file__), 'learning/rules-0.pickle')
search(output_dict, output_rules)