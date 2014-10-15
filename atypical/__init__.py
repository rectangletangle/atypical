""" This package can be used to identify unusual strings/junk data using a combination of the Markov property and
    character ratios.

    Usage (ordered from least typical to most typical):
        >>> list(atypical(['aab', 'abb', 'bb', 'aa', 'ax']).objects())
        ['ax', 'bb', 'aa', 'abb', 'aab']
"""

__version__ = '0.0.0'
__author__  = 'Drew A. French'
__email__   = 'rectangletangle@gmail.com'
__url__     = 'github.com/rectangletangle'

import itertools

from .scoring import Scores, scored
from .metrics import CharMarkov, CharRatio

__all__ = ['CharMarkov', 'CharRatio', 'Scores', 'scored', 'atypical', 'metrics']

METRICS = (CharMarkov, CharRatio)

@scoring.scored
def atypical(strings, metrics=METRICS):
    strings = list(strings)

    trained_metrics = (metric.trained_with(strings) if isinstance(metric, type) else metric
                       for metric in metrics)

    stdscores = itertools.chain(*(metric.scored(strings).standardized()
                                  for metric in trained_metrics))

    seen = set()
    for score, string in sorted(stdscores):
        if string not in seen:
            yield (score, string)
            seen.add(string)
