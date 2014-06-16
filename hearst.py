from multiprocessing import Process, JoinableQueue, Manager
from analysing.hearst_fsm import hearst_patterns
import os
import sys
import pickle

file_list = JoinableQueue()

for root, subFolders, files in os.walk(os.path.join(os.path.dirname(__file__), 'corpus', 'tagged')):
        for current_file in files:
            if current_file.endswith(".pickle"):
                file_list.put(os.path.join(root, current_file))

file_count = file_list.qsize()

hearst_dict = Manager().dict()


def worker():
    while not file_list.empty():
        input_file = file_list.get()

        tagged_data = pickle.load(open(input_file, 'rb'))
        hearst_patterns(tagged_data, hearst_dict)

        percentage = 100.0 - ((float(file_list.qsize()) / float(file_count)) * 100.0)
        sys.stdout.write("\rProgress: {0:.2f}%".format(percentage))
        sys.stdout.flush()

        file_list.task_done()


sys.stdout.write("\rProgress: 0.00%")

for pid in range(1):
    process = Process(target=worker, args=())
    process.daemon = True
    process.start()

file_list.join()
print('')

pickle_dict = dict()

for key in hearst_dict.keys():
    pickle_dict[key] = hearst_dict.get(key)

pickle.dump(pickle_dict, open('corpus/dict.pickle', 'wb+'), 2)
