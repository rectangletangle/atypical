
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
        data = [word for word in f.read().lower().split() if len(word) > 3 and word.isalpha()]

    meanwordlen = statistics.mean(len(word) for word in data)

    print('avg word length:', meanwordlen)

    extra = ['aaaaa',
             'xxxxx',
             'abcde',
             'uuu',
             '<a href="http://example.com">example.com</a>',
             'sdfjhaisjkdls',
             'dsfhsdjkhj',
             ''.join(random.choice(string.ascii_lowercase) for _ in range(int(meanwordlen))),
             ]

    data.extend(extra)

    random.shuffle(data)

    scored = [string for string, score in atypical(data)]

    print('length:', len(scored))

    indexed = [(scored.index(string), string) for string in extra]

    print('percentile:', (max(index for index, _ in indexed) / len(scored)) * 100)

    print()

    pprint(sorted(indexed))

    print()

    pprint(scored[:20])
