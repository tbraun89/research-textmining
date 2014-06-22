import grammars
import find_by_grammar
import time
import os
import pickle


iteration_file = os.path.join(os.path.dirname(__file__), 'learning/iteration')
learning = True


while learning:
    try:
        try:
            with open(iteration_file) as f:
                iteration = int(f.readline())
        except IOError:
            with open(iteration_file, 'w+') as f:
                f.write(str(0))
            iteration = 0

        print('Iteration: ' + str(iteration))

        input_dict = os.path.join(os.path.dirname(__file__), 'learning/dict-' + str(iteration) + '.pickle')
        output_dict = os.path.join(os.path.dirname(__file__), 'learning/dict-' + str(iteration + 1) + '.pickle')
        old_rules = os.path.join(os.path.dirname(__file__), 'learning/rules-' + str(iteration - 1) + '.pickle')
        output_rules = os.path.join(os.path.dirname(__file__), 'learning/rules-' + str(iteration) + '.pickle')

        print('Finding new rules:')
        grammars.learning(input_dict, output_rules)

        time.sleep(5)

        print('Generating new dict:')
        find_by_grammar.search(output_dict, output_rules)

        f = open(iteration_file, 'w')
        f.write(str(iteration + 1))
        f.close()

        if iteration > 0:
            old_rules = pickle.load(open(old_rules, 'rb'))
            new_rules = pickle.load(open(output_rules, 'rb'))

            if old_rules == new_rules:
                print("Done. No new rules found.")

        print("Done. Next iteration in 10 seconds.")
        time.sleep(10)
    except KeyboardInterrupt:
        print('')
        learning = False
