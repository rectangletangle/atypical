
import iterlib

def char_pairs(strings):
    if isinstance(strings, str):
        yield from iterlib.paired(strings)
    else:
        for string in strings:
            yield from iterlib.paired(string)
