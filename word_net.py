import pickle
import nltk
import sys
import os
import pickle
from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import WordNetError

nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk'))

h_dict = pickle.load(open('corpus/dict.pickle', 'rb'))

cleaned = dict()

sys.stdout.write("\rProgress: 0.00%")
current = 0.0

for key in h_dict:
    hypernym = key.lower().replace(' ', '_')

    for word in h_dict[key]:
        possible_hyponym_synset = None

        try:
            possible_hyponym_synset = wordnet.synset(word + '.n.01')
        except WordNetError:
            pass

        if possible_hyponym_synset:
            hypernym_list = list(set([w for s in possible_hyponym_synset.closure(lambda s:s.hyponyms()) for w in s.lemma_names]))

            if hypernym in hypernym_list:
                if hypernym in cleaned:
                    cleaned[hypernym].append(word)
                else:
                    cleaned[hypernym] = [word]

    current += 1.0
    percentage = (current * 100) / float(len(h_dict))

    sys.stdout.write("\rProgress: {0:.2f}%".format(percentage))
    sys.stdout.flush()

pickle.dump(cleaned, open('corpus/dict-0.pickle', 'wb+'), 2)