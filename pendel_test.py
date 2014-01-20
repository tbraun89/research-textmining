from config import config
import pickle

print('Loading dictionary...')

hearst_dict = pickle.load(open(config.HEARST_DICT_FILE, 'rb'))
