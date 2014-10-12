
import statistics

class Scores:
    def __init__(self, name, metric, strings, reverse=False):
        self.name = name
        self.metric = metric
        self.reverse = reverse

        self._strings = strings

    def __iter__(self):
        for string in self._strings:
            yield (string, self.metric(string))

    def ordered(self, iterable=None):
        return sorted(self if iterable is None else iterable, key=lambda pair: pair[1], reverse=self.reverse)

    def strings(self):
        for string, score in self.ordered():
            yield string

    def scores(self):
        for string, score in self.ordered():
            yield score

    def standardized(self):
        strings, scores = zip(*list(self))

        scores = list(scores)
        mean = statistics.mean(scores)
        stdev = statistics.stdev(scores)

        return self.ordered((string, standard_score(score, mean, stdev))
                            for string, score in zip(strings, scores))

def standard_score(raw, mean, stdev):
    return (raw - mean) / stdev
