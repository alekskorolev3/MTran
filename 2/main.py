import re

import tokens


def extract_tokens(line):
    tokens_ = re.findall(tokens.pattern, line)
    return tokens_


with open('/Users/artem/PycharmProjects/MTran/second/2/test.c', 'r') as f:
    text = f.read()

for line in text.splitlines():
    print(extract_tokens(line))
