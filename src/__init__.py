
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
