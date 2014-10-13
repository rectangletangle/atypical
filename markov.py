
import collections
import functools

from .tokens import char_pairs
from .score import scored

def markov(pairs):
    markov_state = collections.defaultdict(functools.partial(collections.defaultdict, int))

    for current, next_ in pairs:
        markov_state[current][next_] += 1

    return markov_state

def score(markov_state, pairs, length):
    total = sum(markov_state[current][next_]
                for current, next_ in pairs)

    try:
        return total / length
    except ZeroDivisionError:
        return 0.0

@scored()
def char_markov(strings, markov_state=None):
    markov_state = markov(char_pairs(strings)) if markov_state is None else markov_state

    for string in set(strings):
        stringscore = score(markov_state, char_pairs(string), len(string))
        yield (stringscore, string)

if __name__ == '__main__':
    trained = markov(char_pairs(['ababac']))

    assert trained['a']['b'] == 2
    assert trained['b']['a'] == 2
    assert trained['a']['c'] == 1
    assert trained['c']['a'] == 0

    strings = ['ab', 'ababac', 'xxx', 'fsdfab']

    assert score(trained, '', 0) == 0.0

    chars = char_markov(strings, trained)

    assert chars.name == 'char-markov'
    assert list(chars.ordered().objects()) == ['xxx', 'fsdfab', 'ab', 'ababac']

