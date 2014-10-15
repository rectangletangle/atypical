
import statistics
import random
import string
import os

import atypical

def sample_words():
    pkg_root = os.path.dirname(os.path.dirname(__file__))
    sample = os.path.join(pkg_root, 'data', 'wikisample.txt')

    with open(sample, encoding='utf-8') as f:
        return [word for word in f.read().lower().split()
                if len(word) > 4 and word.isalpha()]

def output(words, atypicalwords, indexed):
    indent = ' ' * 3

    print('corpus length (words):', len(words))
    print('unique words:', len(atypicalwords))
    print()

    print('percentile:', (max(index for index, _ in indexed) / len(atypicalwords)) * 100)
    print()

    print('junk data indexes:')
    for index, word in sorted(indexed):
        print(indent, index, word.encode('unicode-escape').decode())
    print()

    print('most typical:')
    for stdscore, word in reversed(list(atypicalwords)[-5:]):
        print(indent, '{:.4f}'.format(stdscore), word.encode('unicode-escape').decode())
    print()

    print('least typical:')
    for stdscore, word in list(atypicalwords)[:15]:
        print(indent, '{:.4f}'.format(stdscore), word.encode('unicode-escape').decode())

if __name__ == '__main__':
    random.seed(0)

    words = sample_words()

    meanwordlen = statistics.mean(len(word) for word in words)

    junkdata = [
                'aaaaa',
                'xxxxx',
                'uuuuu',
                'eeeee',
                'sdfjhsjkdls',
                'dsfhsdjkhj',
                ''.join(random.choice(string.ascii_lowercase) for _ in range(int(meanwordlen))),
                '<a href="http://www.example.com">http://www.example.com</a>'
               ]

    words.extend(junkdata)
    random.shuffle(words)

    metrics = (
               atypical.CharMarkov,
               atypical.CharRatio,
              )

    atypicalwords = atypical.atypical(words, metrics=metrics).sorted()

    indexed = [(list(atypicalwords.objects()).index(string), string) for string in junkdata]

    output(words, atypicalwords, indexed)
