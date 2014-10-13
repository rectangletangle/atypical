
import collections
import statistics
import itertools

from .markov import char_markov
from .ratio import char_ratio
from .score import scored

metrics = (
           char_markov,
           char_ratio,
          )

@scored()
def atypical(strings, metrics=metrics):
    strings = list(strings)

    stdscores = itertools.chain(*(metric(strings).standardized() for metric in metrics))

    seen = set()
    for score, string in sorted(stdscores):
        if string not in seen:
            yield (score, string)
            seen.add(string)

@scored()
def composite(strings, metrics=metrics):
    strings = list(strings)

    subscores = collections.defaultdict(list)

    for metric in metrics:
        for stdscore, token in metric(strings).standardized():
            subscores[token].append(stdscore)

    for token, stdscores in subscores.items():
        composite_score = statistics.mean(stdscores)
        yield (composite_score, token)
