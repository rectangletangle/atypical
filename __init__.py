
import collections
import statistics

from . import markov, charratio

def atypical(strings, metrics=(markov.scored,)):
    tokens = set(string.lower() for string in strings)

    subscores = collections.defaultdict(list)

    for metric in metrics:
        for token, stdscore in metric(tokens).standardized():
            subscores[token].append(stdscore)

    composite = {token: statistics.mean(stdscores)
                 for token, stdscores in subscores.items()}

    return sorted(composite.items(), key=lambda pair: pair[1])
