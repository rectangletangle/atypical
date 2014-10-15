
import unittest
import random

from .metrics import CharMarkov, CharRatio
from .scoring import Scores
from . import atypical

class _TestMetric:
    def test_untrained(self):
        self.assert_empty_scores(['a', 'b', 'c'])

    def test_train_empty(self):
        self.metric.train([])
        self.assert_empty_scores(['a', 'b', 'c'])

    def test_score_empty(self):
        self.metric.train(['a', 'b', 'c'])
        self.assert_empty_scores([])

    def assert_empty_scores(self, strings):
        self.assertEqual([(0.0, string) for string in strings],
                         list(self.metric.scored(strings).standardized().sorted()))

    def test_longer_isnt_worse(self):
        scored = self.metric.scored(['zzz', 'zzzz']).sorted()

        self.assertTrue(len(set(scored.scores())) == 1) # Asserts all scores are the same.
        self.assertEqual(['zzz', 'zzzz'], list(scored.objects()))

class TestMarkov(unittest.TestCase, _TestMetric):
    def setUp(self):
        self.metric = CharMarkov()
        self.training_data = ['ab'] * 4 + ['ac'] * 2 + ['xx']

        random.shuffle(self.training_data) # Training data order shouldn't matter.

    def test_train(self):
        self.metric.train(self.training_data)
        self.assert_order(['xx', 'ac', 'ab'])
        self.metric.train(['xx'] * 2)
        self.assert_order(['ac', 'xx', 'ab'])
        self.metric.train(['xx'] * 2)
        self.assert_order(['ac', 'ab', 'xx'])
        self.metric.train(['ab'] * 2)
        self.assert_order(['ac', 'xx', 'ab'])

    def assert_order(self, strings):
        self.assertEqual(strings,
                         list(self.metric.scored(strings).sorted().objects()))

class TestRatio(unittest.TestCase, _TestMetric):
    def setUp(self):
        self.metric = CharRatio()
        self.data = ['xxx', 'aab', 'abb', 'aabb']

        random.shuffle(self.data)

    def test_train(self):
        self.metric.train(['aa', 'b'])
        self.assert_scores((0.0, 'aab'), (-1.0, 'xxx'), ['xxx', 'abb', 'aabb', 'aab'])
        self.metric.train(['b'])
        self.assert_scores((0.0, 'aabb'), (-1.0, 'xxx'), ['xxx', 'aab', 'abb', 'aabb'])
        self.metric.train(['xxxxxxxx'])
        self.assert_scores(None, None, ['aab', 'abb', 'aabb', 'xxx'])

    def assert_scores(self, best, worst, strings):
        scored = self.metric.scored(self.data).sorted()

        if best:
            self.assertEqual(best, list(scored)[-1])

        if worst:
            self.assertEqual(worst, list(scored)[0])

        self.assertEqual(strings, list(scored.objects()))

class TestScores(unittest.TestCase):
    def setUp(self):
        self.scores = Scores([(-1, 'c'), (0.25, 'b'), (0, 'a')])

    def test_sorting(self):
        # All sorting is based on the object's scores, not the objects themselves.
        self.assert_scores(['c', 'a', 'b'], self.scores.sorted().objects())
        self.assert_scores(['b', 'a', 'c'], self.scores.reversed().objects())

        reversedscores = reversed(self.scores)
        self.assertTrue(isinstance(reversedscores, list))
        self.assert_scores([(0.25, 'b'), (0, 'a'), (-1, 'c')], reversedscores)

    def test_length(self):
        self.assertEqual(3, len(self.scores))

        iter_ = zip([2, 1], 'ba')
        self.assertRaises(TypeError, lambda: len(iter_))

        iterscores = Scores(iter_)
        self.assertEqual(2, len(iterscores))
        self.assert_scores([(1.0, 'a'), (2.0, 'b')], iterscores.sorted())

    def test_scores_iter(self):
        self.assert_scores([-1.0, 0.25, 0.0], self.scores.scores())

    def test_objects_iter(self):
        self.assert_scores(['c', 'b', 'a'], self.scores.objects())

    def test_standardized(self):
        self.assert_scores([(-1.1339, 'c'), (0.7559, 'b'), (0.378, 'a')],
                           [(round(score, 4), object_) for score, object_ in self.scores.standardized()])

    def test_empty(self):
        emptyscores = Scores([])

        self.assert_scores([], emptyscores)
        self.assert_scores([], emptyscores.objects())
        self.assert_scores([], emptyscores.scores())
        self.assert_scores([], emptyscores.sorted())
        self.assert_scores([], emptyscores.reversed())
        self.assert_scores([], emptyscores.standardized())

        self.assertEqual(0, len(emptyscores))

    def assert_scores(self, correct, scores):
        self.assertEqual(list(correct), list(scores))

class TestAtypical(unittest.TestCase):
    def setUp(self):
        self.strings = ['aa', 'ab', 'aa', 'abab', 'ac', 'xx']

    def test(self):
        self.assertEqual(['xx', 'ac', 'aa'], self.atypical_strings()[:3])

    def test_mixed(self):
        mixedmetrics = [CharMarkov.trained_with(self.strings), CharRatio]

        self.assertEqual(list(atypical(self.strings).sorted()),
                         list(atypical(self.strings, metrics=mixedmetrics).sorted()))

    def test_pretrained(self):
        self.assertEqual(['xx'],
                         self.atypical_strings(metrics=[CharMarkov.trained_with(['xx'])])[-1:])

    def atypical_strings(self, *args, **kw):
        return list(atypical(self.strings, *args, **kw).sorted().objects())

