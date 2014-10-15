
import statistics
import functools

try:
    import represent # Nice to have, but not entirely necessary.
except ImportError:
    ...

class Scores:
    def __init__(self, scored_objects):
        self._scored_objects = list(scored_objects)

    def __repr__(self, *args, **kw):
        try:
            return represent.literal(self, list(self))
        except NameError:
            return super().__repr__()

    def __iter__(self):
        for score, object_ in self._scored_objects:
            yield (float(score), object_)

    def __len__(self):
        return len(self._scored_objects)

    def __reversed__(self):
        return list(self.reversed())

    def scores(self):
        for score, _ in self:
            yield score

    def objects(self):
        for _, object_ in self:
            yield object_

    def sorted(self):
        return self._clone(sorted(self))

    def reversed(self):
        return self._clone(sorted(self, reverse=True))

    def standardized(self):
        try:
            scores, objects = zip(*list(self))
        except ValueError:
            standardized_scores = []
        else:
            scores = list(scores)
            mean = statistics.mean(scores)
            stdev = statistics.stdev(scores)

            standardized_scores = ((standard_score(score, mean, stdev), object_)
                                   for score, object_ in zip(scores, objects))

        return self._clone(standardized_scores)

    def rounded(self, *args, ndigits=3, **kw):
        return self._clone((round(score, ndigits=ndigits, *args, **kw), object_)
                           for score, object_ in self)

    def _clone(self, newscores):
        return self.__class__(newscores)

def standard_score(raw, mean, stdev):
    try:
        return (raw - mean) / stdev
    except ZeroDivisionError:
        return 0.0

def scored(generator):
    @functools.wraps(generator)
    def wrapper(*args, **kw):
        return Scores(generator(*args, **kw))
    return wrapper

