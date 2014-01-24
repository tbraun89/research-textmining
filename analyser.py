from analysing.np_multi import corpus_analyser
from config import config
import pickle

multi_dict = corpus_analyser(config.CORPUS_PATH, config.PROCESS_COUNT)
hearst_dict = dict()

print('Saving dictionary...\n')


for key in multi_dict.keys():
    hearst_dict[key] = multi_dict.get(key)

pickle.dump(hearst_dict, open(config.HEARST_DICT_FILE, 'wb+'), 2)

hyper_count = 0
hypo_count = 0

for element in hearst_dict:
    hyper_count += 1
    hypo_count += len(element)

print "Hypernyms:\t\t" + str(hyper_count)
print "Hyponyms:\t\t" + str(hypo_count)