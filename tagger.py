# TODO test with Jython (compile to java)
# TODO pypy
# TODO freeze

from multiprocessing import Process, JoinableQueue
import nltk
import os
import sys
import re
import pickle

nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk'))

file_list = JoinableQueue()

for root, subFolders, files in os.walk(os.path.join(os.path.dirname(__file__), 'corpus', 'plain')):
        for current_file in files:
            if current_file.endswith(".txt"):
                file_list.put(os.path.join(root, current_file))

file_count = file_list.qsize()


def worker():
    while not file_list.empty():
        input_file = file_list.get()

        with open(input_file, 'r') as c_file:
            contents = c_file.read()
            contents = contents.replace(' {2,}', '')
            contents = re.sub('\s{2,}', ' ', contents)

        tokens = [word for sent in nltk.sent_tokenize(contents) for word in nltk.word_tokenize(sent)]
        pos_tagged = nltk.pos_tag(tokens)
        pos_tagged = nltk.ne_chunk(pos_tagged)

        tagged_list = []

        for child in pos_tagged:
            if isinstance(child, nltk.tree.Tree):
                t_content = ''

                for t_child in child:
                    t_content += t_child[0] + ' '
                tagged_list.append((t_content.rstrip(), 'NE'))

            else:
                tagged_list.append(child)

        output_file = os.path.splitext(os.path.basename(input_file))[0] + '.pickle'
        output_file = os.path.join(os.path.dirname(__file__), 'corpus', 'tagged', output_file)

        pickle.dump(tagged_list, open(output_file, 'wb+'), 2)

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
