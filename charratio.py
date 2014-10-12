
import collections
import functools

from .score import Scores

def charratios(strings):
    charcount = collections.Counter()
    for string in strings:
        for char in string:
            charcount[char] += 1

    total = sum(charcount.values())

    ratios = collections.defaultdict(float)
    for char, count in charcount.items():
        ratios[char] = count / total

    return ratios

def score(ratios, string):
    termratios = charratios([string])
    return sum(termratios[char] - ratios[char] for char in set(string))

def scored(strings, trained=None):
    if trained is None:
        trained = charratios(strings)

    return Scores('charratio', functools.partial(score, trained), strings, reverse=True)

if __name__ == '__main__':
    ratios = charratios(['aab', 'abb', 'aab'])

    assert round(ratios['a'], 1) == 0.6
    assert round(ratios['b'], 1) == 0.4
    assert ratios['c'] == 0.0
    assert ratios['a'] + ratios['b'] == 1.0

    assert charratios([])['a'] == 0.0 # empty test

    strings = ['aab', 'abb', 'aab', 'ca', 'cccc', 'zz', 'zaa', 'x']
    ratios = charratios(strings)
    assert list(scored(strings, ratios).strings())[:3] == ['x', 'zz', 'cccc']


