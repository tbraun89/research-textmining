from analysing.np_multi import corpus_analyser
from config import config
import pickle

multi_dict = corpus_analyser(config.CORPUS_PATH, config.PROCESS_COUNT)
hearst_dict = dict()

print('Saving dictionary...')

for key in multi_dict.keys():
    hearst_dict[key] = multi_dict.get(key)

print hearst_dict

pickle.dump(hearst_dict, open(config.HEARST_DICT_FILE, 'wb+'), 2)
