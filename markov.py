
import collections
import functools

import iterlib

__all__ = ['train', 'score', 'atypical']

def train(strings):
    state = collections.defaultdict(lambda: collections.defaultdict(int))

    for string in strings:
        for currentchar, nextchar in iterlib.paired(string):
            state[currentchar.lower()][nextchar.lower()] += 1

    return state

def score(trained, string):
    total = sum(trained[currentchar.lower()][nextchar.lower()]
                for currentchar, nextchar in iterlib.paired(string))

    try:
        return total / len(string)
    except ZeroDivisionError:
        return 0.0

def atypical(trained, strings):
    return sorted(strings, key=functools.partial(score, trained))

if __name__ == '__main__':
    trained = train(['ababac'])

    assert trained['a']['b'] == 2
    assert trained['b']['a'] == 2
    assert trained['a']['c'] == 1
    assert trained['c']['a'] == 0

    strings = ['ab', 'ababac', 'xxx', 'fsdfab']

    assert score(trained, '') == 0.0

    assert atypical(trained, strings) == ['xxx', 'fsdfab', 'ab', 'ababac']

