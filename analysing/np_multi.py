import os
import nltk
from nltk import word_tokenize, pos_tag
from multiprocessing import Process, JoinableQueue, Manager
from analysing.hearst_fsm import hearst_patterns


nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk_data'))


def corpus_analyser(corpus_path, process_count):
    print('Scanning corpora...')

    file_queue = JoinableQueue()
    hearst_dict = Manager().dict()

    for root, subFolders, files in os.walk(corpus_path):
        for current_file in files:
            if current_file.endswith(".txt"):
                file_queue.put(os.path.join(root, current_file))

    print "{0} files found.".format(file_queue.qsize())

    def worker(process_id):
        while not file_queue.empty():
            current_path = file_queue.get()
            print 'Processing (Process-{1}) "{0}"'.format(current_path, process_id)

            with open(current_path, 'r') as current_file:
                data = ' '.join(current_file.read().replace('\n', ' ').split())

            data_tagged = pos_tag(word_tokenize(data))
            hearst_patterns(data_tagged, hearst_dict)

            file_queue.task_done()

    for pid in range(process_count):
        process = Process(target=worker, args=(pid,))
        process.daemon = True
        process.start()

    file_queue.join()

    return hearst_dict





