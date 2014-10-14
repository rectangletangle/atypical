
import statistics
import random
import string
import os

from . import atypical

from pprint import pprint

if __name__ == '__main__':
    random.seed(0)

    path = os.path.split(__file__)[0]
    sample = os.path.join(path, 'data', 'sample.txt')

    with open(sample) as f:
        words = [word for word in f.read().lower().split()
                 if len(word) > 4 and word.isalpha()]

    meanwordlen = statistics.mean(len(word) for word in words)

    extra = ['aaaaa',
             'xxxxx',
             'uuuuu',
             'eeeee',

             'sdfjhaisjkdls',
             'dsfhsdjkhj',
             ''.join(random.choice(string.ascii_lowercase) for _ in range(int(meanwordlen))),

             #'abcde',
             #'<a href="http://example.com">example.com</a>',
             ]

    words.extend(extra)
    random.shuffle(words)

    atypical_words = atypical(words).ordered()

    objects = list(atypical_words.objects())
    indexed = [(objects.index(string), string) for string in extra]

    print('corpus length:', len(words))
    print('scored length:', len(atypical_words))
    print()

    print('percentile:', (max(index for index, _ in indexed) / len(atypical_words)) * 100)
    print()

    print('indexes:')
    pprint(sorted(indexed))
    print()

    print('first ten:')
    pprint(list(atypical_words)[:20])
    print()

