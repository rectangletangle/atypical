
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
        self._total = self._count_chars(self._counter, (char for string in strings for char in string))

    def score(self, string):
        string_counter = collections.Counter()
        string_total = self._count_chars(string_counter, string)

        char_ratios = ((self._ratio(self._counter, char, self._total),
                        self._ratio(string_counter, char, string_total))
                       for char in string)

        char_ratio_diff = sum(global_ratio - string_ratio
                              for global_ratio, string_ratio in char_ratios)

        return char_ratio_diff / len(string)

    def _ratio(self, counter, char, total):
        try:
            return counter[char] / total
        except ZeroDivisionError:
            return 0.0

    def _count_chars(self, counter, chars):
        for char in chars:
            counter[char] += 1
        return sum(counter.values())
