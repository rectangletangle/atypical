
import statistics
import functools

import represent

class Scores:
    def __init__(self, scored_objects, name=None):
        self.name = name

        self._scored_objects = scored_objects

    def __repr__(self, *args, **kw):
        return represent.literal(self, list(self), **self._options())

    def __iter__(self):
        yield from self._scored_objects

    def __len__(self):
        try:
            return len(self._scored_objects)
        except TypeError:
            self._eval()
            return len(self._scored_objects)

    def __reversed__(self):
        return self.reversed()

    def scores(self):
        for score, _ in self:
            yield score

    def objects(self):
        for _, object_ in self:
            yield object_

    def ordered(self):
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

    def _eval(self):
        if not isinstance(self._scored_objects, list):
            self._scored_objects = list(self._scored_objects)

    def _options(self):
        return {'name': self.name}

    def _clone(self, newscores):
        return self.__class__(newscores, **self._options())

def standard_score(raw, mean, stdev):
    return (raw - mean) / stdev

def scored(**kw):
    def wrapper(generator):
        @functools.wraps(generator)
        def wrapper_(*generator_args, **generator_kw):
            kw.setdefault('name', generator.__name__.strip('_').replace('_', '-'))
            return Scores(generator(*generator_args, **generator_kw), **kw)
        return wrapper_
    return wrapper
