
import collections
import functools

import iterlib

from .score import Scores

def markov(strings):
    state = collections.defaultdict(functools.partial(collections.defaultdict, int))

    for string in strings:
        for currentchar, nextchar in iterlib.paired(string):
            state[currentchar][nextchar] += 1

    return state

def score(trained, string):
    total = sum(trained[currentchar][nextchar]
                for currentchar, nextchar in iterlib.paired(string))

    try:
        return total / len(string)
    except ZeroDivisionError:
        return 0.0

def scored(strings, trained=None):
    if trained is None:
        trained = markov(strings)

    return Scores('markov', functools.partial(score, trained), strings)

if __name__ == '__main__':
    trained = markov(['ababac'])

    assert trained['a']['b'] == 2
    assert trained['b']['a'] == 2
    assert trained['a']['c'] == 1
    assert trained['c']['a'] == 0

    strings = ['ab', 'ababac', 'xxx', 'fsdfab']

    assert score(trained, '') == 0.0

    assert list(scored(strings, trained).strings()) == ['xxx', 'fsdfab', 'ab', 'ababac']

