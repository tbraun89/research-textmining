import pickle
import random

h_dict = pickle.load(open('corpus/dict.pickle', 'rb'))

rnd_keys = random.sample(h_dict, 100)

for c_key in rnd_keys:
    out_str = c_key + ' ~> ' + ', '.join(h_dict[c_key])
    print(out_str)

