import re

import tokens


def extract_tokens(text):

    l = []

    for index, line in enumerate(text.splitlines()):
        for match in re.finditer(tokens.pattern, line):
            l.append((index, match.start(), match.group()))

    return l





with open('/Users/artem/PycharmProjects/MTran/second/2/test.c', 'r') as f:
    text = f.read()


print(extract_tokens(text))


