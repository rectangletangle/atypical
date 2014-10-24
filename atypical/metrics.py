
import collections
import functools

import iterlib

from . import scoring

class Metric:
    @classmethod
    def trained_with(cls, objects):
        instance = cls()
        instance.train(objects)
        return instance

    def train(self, objects):
        """ Train the metric. """

        raise NotImplementedError

    def score(self, object_) -> float:
        """ Score an individual object. """

        raise NotImplementedError

    @scoring.scored
    def scored(self, objects) -> scoring.Scores:
        """ Score the given objects relative to the trained state. """

        for object_ in set(objects):
            yield (self.score(object_), object_)

class CharMarkov(Metric):
    def __init__(self):
        self._state = collections.defaultdict(functools.partial(collections.defaultdict, int))

    def train(self, strings):
        for current, next_ in self._transition_pairs(strings):
            self._state[current][next_] += 1

    def score(self, string):
        occurrences = sum(self._state[current][next_]
                          for current, next_ in self._transition_pairs([string]))

        try:
            return occurrences / len(string)
        except ZeroDivisionError:
            return 0.0

    def _transition_pairs(self, strings):
        for string in strings:
            yield from iterlib.paired(string)

class CharRatio(Metric):
    def __init__(self):
        self._counter = collections.Counter()
        self._total = 0

    def train(self, strings):
        self._count_chars(self._counter, (char for string in strings for char in string))
        self._total = self._total_count(self._counter)

    def score(self, string):
        string_counter = collections.Counter()
        self._count_chars(string_counter, string)
        string_total = self._total_count(string_counter)

        char_ratios = [(self._ratio(self._counter, self._total, char),
                        self._ratio(string_counter, string_total, char))
                       for char in set(string)]

        assert round(sum(string_ratio for _, string_ratio in char_ratios), 6) == 1.0

        return sum(abs(global_ratio - string_ratio)
                   for global_ratio, string_ratio in char_ratios) * -1

    def _ratio(self, counter, total, char):
        try:
            return counter[char] / total
        except ZeroDivisionError:
            return 0.0

    def _total_count(self, counter):
        return sum(counter.values())

    def _count_chars(self, counter, chars):
        for char in chars:
            counter[char] += 1
