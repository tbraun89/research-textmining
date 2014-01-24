import os
import nltk
import sys
from nltk import word_tokenize, pos_tag
from multiprocessing import Process, JoinableQueue, Manager, Value
from analysing.hearst_fsm import hearst_patterns


nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk_data'))


def corpus_analyser(corpus_path, process_count):
    print('Scanning corpora...')

    file_queue = JoinableQueue()
    hearst_dict = Manager().dict()
    word_count = Value('i', 0)

    for root, subFolders, files in os.walk(corpus_path):
        for current_file in files:
            if current_file.endswith(".txt"):
                file_queue.put(os.path.join(root, current_file))

    file_count = file_queue.qsize()
    print "{0} files found.\n".format(file_count)

    sys.stdout.write("\r0.00%\tWord count: 0")

    def worker(process_id):
        while not file_queue.empty():
            current_path = file_queue.get()

            with open(current_path, 'r') as current_file:
                data = ' '.join(current_file.read().replace('\n', ' ').split())

            data_tokenized = word_tokenize(data)
            word_count.value += len(data_tokenized)

            data_tagged = pos_tag(data_tokenized)
            hearst_patterns(data_tagged, hearst_dict)

            percentage = 100.0 - ((float(file_queue.qsize()) / float(file_count)) * 100.0)
            sys.stdout.write("\r{0:.2f}%\tWord count: {1}".format(percentage, word_count.value))
            sys.stdout.flush()

            file_queue.task_done()

    for pid in range(process_count):
        process = Process(target=worker, args=(pid,))
        process.daemon = True
        process.start()

    file_queue.join()
    print "\n"

    return hearst_dict





