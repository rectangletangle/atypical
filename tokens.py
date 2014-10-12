
def tokenized(strings):
    for string in strings:
        for token in string.lower().split():
            yield token

