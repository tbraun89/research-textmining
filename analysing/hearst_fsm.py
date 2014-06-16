import abc


POS_LIST = ['NN', 'NNS', 'NNP', 'NNPS', 'NE']


class State():
    __metaclass__ = abc.ABCMeta

    START = 0
    NN_F0 = 1
    NN_F0_CONNECTION0 = 2
    NN_F0_CONNECTION1 = 3
    NN_F0_CONNECTION2 = 7
    NN_F0_CONNECTION3 = 8
    NN_B0 = 4
    NN_B0_CONNECTION = 5
    NN_B1 = 9
    BACK_TO_NN_B0_HELPER = 6


def hearst_patterns(data_tagged, hearst_dict):
    state = State.START
    hypernym0 = ''
    hypernym1 = ''
    hyponym_list0 = set()
    hyponym_list1 = set()

    def add_to_dict(val):
        if val == 0:
            old_hyponym_list = hearst_dict.get(hypernym0)
        elif val == 1:
            old_hyponym_list = hearst_dict.get(hypernym1)

        if old_hyponym_list is None:
            old_hyponym_list = set()

        if val == 0:
            new_hyponym_list = old_hyponym_list.union(hyponym_list0)
            hearst_dict[hypernym0] = new_hyponym_list
        elif val == 1:
            new_hyponym_list = old_hyponym_list.union(hyponym_list1)
            hearst_dict[hypernym1] = new_hyponym_list

    for element in data_tagged:
        if state == State.BACK_TO_NN_B0_HELPER:
            state = State.NN_B0

        if state == State.NN_B0_CONNECTION:
            if element[1] in POS_LIST:
                hyponym_list0.add(element[0])
                state = State.BACK_TO_NN_B0_HELPER
            else:
                add_to_dict(0)
                state = State.START

        elif state == State.NN_B0:
            if element[0] in [',', 'or', 'and']:
                state = State.NN_B0_CONNECTION
            else:
                add_to_dict(0)
                state = State.START

        elif state == State.NN_F0_CONNECTION1:
            if element[1] in POS_LIST:
                hyponym_list0.add(element[0])
                state = State.NN_B0
            else:
                state = State.START

        elif state == State.NN_F0_CONNECTION0:
            if element[0] == 'as':
                state = State.NN_F0_CONNECTION1
            else:
                state = State.START

        elif state == State.NN_B1:
            if element[1] in POS_LIST:
                hypernym1 = element[0]
                add_to_dict(1)
            else:
                state = State.START

        elif state == State.NN_F0_CONNECTION3:
            if element[0] == 'other':
                state = State.NN_B1
            else:
                state = State.START

        elif state == State.NN_F0_CONNECTION2:
            if element[0] == 'such':
                state = State.NN_F0_CONNECTION0
            elif element[0] in ('like', 'including', 'especially'):
                state = State.NN_F0_CONNECTION1
            elif element[1] == ',':
                state = State.NN_F0_CONNECTION2
            elif element[1] in POS_LIST:
                hyponym_list1.add(element[0])
            elif element[0] in ('and', 'or'):
                state = State.NN_F0_CONNECTION3
            else:
                state = State.START

        elif state == State.NN_F0:
            if element[0] == 'such':
                state = State.NN_F0_CONNECTION0
            elif element[0] in ('like', 'including', 'especially'):
                state = State.NN_F0_CONNECTION1
            elif element[1] == ',':
                state = State.NN_F0_CONNECTION2
            else:
                state = State.START

        elif state == State.START:
            hypernym0 = ''
            hypernym1 = ''
            hyponym_list0.clear()
            hyponym_list1.clear()

            if element[1] in POS_LIST:
                state = State.NN_F0
                hypernym0 = element[0]
                hyponym_list1.add(element[0])