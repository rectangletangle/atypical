
import random
import os

from . import atypical

if __name__ == '__main__':
    path = os.path.split(__file__)[0]
    sample = os.path.join(path, 'data', 'sample.txt')

    with open(sample) as f:
        data = [word for word in f.read().lower().split() if len(word) > 3 and word.isalpha()]

    extra = ['aaaaa', 'xxxxx', 'abcd', 'uuu']

    data.extend(extra)

    random.shuffle(data)

    scored = [string for string, score in atypical(data)]

    for string in extra:
        print(string, scored.index(string))

    from pprint import pprint

    pprint(scored[:10])
