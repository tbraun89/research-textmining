import pickle
import os
from nltk import word_tokenize

HEARST_DICT_FILE = os.path.join(os.path.dirname(__file__), 'data/hearst-OANC.dict')
CORPOS_PATH = '/home/tbraun/Downloads/corpora'

hearst_dict = pickle.load(open(HEARST_DICT_FILE, 'rb'))

hyper_count = 0
hypo_count = 0
corp_size = 0
for element in hearst_dict:
    hyper_count += 1
    hypo_count += len(element)

for root, subFolders, files in os.walk(CORPOS_PATH):
    for current_file in files:
        if current_file.endswith(".txt"):
            with open(os.path.join(root, current_file), 'r') as current_file:
                data = ' '.join(current_file.read().replace('\n', ' ').split())
                corp_size += len(word_tokenize(data))

print "Corpus size:\t" + str(corp_size)
print "Hypernyms:\t\t" + str(hyper_count)
print "Hyponyms:\t\t" + str(hypo_count)