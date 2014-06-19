import grammars
import time
import os


iteration_file = os.path.join(os.path.dirname(__file__), 'learning/iteration')
learning = True


while learning:
    try:
        with open(iteration_file) as f:
            iteration = int(f.readline())

        print('Iteration: ' + str(iteration))

        input_dict = os.path.join(os.path.dirname(__file__), 'learning/dict-' + str(iteration) + '.pickle')
        output_rules = os.path.join(os.path.dirname(__file__), 'learning/rules-' + str(iteration) + '.pickle')

        print('Finding new rules:')
        grammars.learning(input_dict, output_rules)

        print('Generating new dict: (TODO)')

        f = open(iteration_file, 'w')
        f.write(str(iteration + 1))
        f.close()

        print("Done. Next round in 10 seconds.")
        time.sleep(10)
    except KeyboardInterrupt:
        print('')
        learning = False