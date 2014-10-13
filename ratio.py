
import collections

from .score import scored

def ratios(objects):
    object_count = collections.Counter()

    for object_ in objects:
        object_count[object_] += 1

    total = sum(object_count.values())

    ratio_state = collections.defaultdict(float)

    for object_, count in object_count.items():
        ratio_state[object_] = count / total

    return ratio_state

def score(ratio_state, string):
    ratios_for_string = ratios(string)
    return -1 * sum(ratios_for_string[char] - ratio_state[char] for char in set(string))

@scored()
def char_ratio(strings, ratio_state=None):
    if ratio_state is None:
        ratio_state = ratios(char for string in strings for char in string)

    for string in set(strings):
        char_ratio_score = score(ratio_state, string)
        yield (char_ratio_score, string)

if __name__ == '__main__':
    ratio_state = ratios('aababbaab')

    assert round(ratio_state['a'], 1) == 0.6
    assert round(ratio_state['b'], 1) == 0.4
    assert ratio_state['c'] == 0.0
    assert ratio_state['a'] + ratio_state['b'] == 1.0

    assert ratios([])['a'] == 0.0 # empty test

    strings = ['aab', 'abb', 'aab', 'ca', 'cccc', 'zz', 'zaa', 'x']
    ratio_state = ratios(char for string in strings for char in string)

    assert list(char_ratio(strings, ratio_state).ordered().objects())[:3] == ['x', 'zz', 'cccc']

