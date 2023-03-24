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

identifiers_table = []
constants_table = []
keywords_table = []
datatypes_table = []
operators_table = []
directives_table = []
functions_table = []

set_of_tokens = extract_tokens(text)

_func = False

for i, token in enumerate(set_of_tokens):

    if token[2] in tokens.keywords:
        if set_of_tokens[i - 1][2] not in tokens.datatypes:
            keywords_table.append((token[2], tokens.keywords[token[2]]))
            continue
        else:
            raise SyntaxError("You cannot use keywords as identifiers!" + str(token[0]) + str(token[1]))

    if token[2] in tokens.datatypes:
        datatypes_table.append((token[2], tokens.datatypes[token[2]]))
        continue
    if token[2] in tokens.functions:
        functions_table.append((token[2], tokens.functions[token[2]]))
        continue
    if token[2] in directives_table:
        directives_table.append((token[2], tokens.directives[token[2]]))
        continue

    if set_of_tokens[i - 1][2] == ")":
        _func = False

    if re.search(tokens.string_pattern.pattern, token[2]):
        if set_of_tokens[i - 1][2] in tokens.operators:
            constants_table.append((token[2], "Constant of string type"))
            continue
        elif _func:
            constants_table.append((token[2], "Constant"))
            continue
        elif set_of_tokens[i - 1][2] == "return":
            constants_table.append((token[2], "Constant"))
            continue
        else:
            raise SyntaxError(
                str(token[0] + 1) + ":" + str(token[1]) + " Error: Expected identifier before constant")

    if re.search(tokens.char_pattern.pattern, token[2]):
        if set_of_tokens[i - 1][2] in tokens.operators:
            constants_table.append((token[2], "Constant of char type"))
            continue
        elif _func:
            constants_table.append((token[2], "Constant"))
            continue
        elif set_of_tokens[i - 1][2] == "return":
            constants_table.append((token[2], "Constant"))
            continue
        else:
            raise SyntaxError(
                str(token[0] + 1) + ":" + str(token[1]) + " Error: Expected identifier before constant")

    if re.search(tokens.identifier_pattern.pattern, token[2]):
        if token[2] not in identifiers_table:
            if set_of_tokens[i + 1][2] == "(":
                _func = True
                functions_table.append(token[2])
            elif set_of_tokens[i - 1][2] in tokens.datatypes:
                identifiers_table.append(token[2])
                continue
            else:
                raise SyntaxError("Undefined identifier " + str(token[0]) + " " + str(token[1]))
        else:
            if set_of_tokens[i - 1][2] in tokens.datatypes:
                raise SyntaxError("Duplicat identifier " + str(token[0]) + str(token[1]))

    if token[2] in tokens.operators:
        if token[2] == '++':
            if set_of_tokens[i - 1][2] in identifiers_table or set_of_tokens[i + 1][2] in identifiers_table:
                operators_table.append((token[2], tokens.operators[token[2]]))
                continue
            else:
                raise SyntaxError(str(token[0]) + " " + str(token[1]) + " Expected identifier before '" + str(token[2]) + "' token")

        if not set_of_tokens[i - 1][2] in identifiers_table:
            raise SyntaxError(str(token[0]) + " " + str(token[1]) + " Expected identifier before '" + str(token[2]) + "' token")
        else:
            operators_table.append((token[2], tokens.operators[token[2]]))
            continue

    if re.search(tokens.float_pattern.pattern, token[2]):
        if set_of_tokens[i - 1][2] in tokens.operators:
            constants_table.append((token[2], "Constant of float type"))
            continue
        elif _func:
            constants_table.append((token[2], "Constant"))
            continue
        elif set_of_tokens[i - 1][2] == "return":
            constants_table.append((token[2], "Constant"))
            continue
        else:
            raise SyntaxError(
                str(token[0] + 1) + ":" + str(token[1]) + " Error: Expected identifier before constant")

    if re.search(tokens.int_pattern.pattern, token[2]):
        if set_of_tokens[i - 1][2] in tokens.operators:
            constants_table.append((token[2], "Constant of int type"))
            continue
        elif _func:
            constants_table.append((token[2], "Constant of int type"))
            continue
        elif set_of_tokens[i - 1][2] == "return":
            constants_table.append((token[2], "Constant of int type"))
            continue
        else:
            raise SyntaxError(
                str(token[0] + 1) + ":" + str(token[1]) + " Error: Expected identifier before constant")



print("Identifiers", identifiers_table)
print("Constants", constants_table)
print("Keywords", keywords_table)
print("Functions", functions_table)
print("Datatypes", datatypes_table)
print("Operators", operators_table)
print("Directives", directives_table)

# if re.search(tokens.char_pattern.pattern, token[2]):
#     constants_table.append((token[2], "Char value"))
#     continue
# if re.search(tokens.float_pattern.pattern, token[2]):
#     constants_table.append((token[2], "Float value"))
#     continue
# if re.search(tokens.string_pattern.pattern, token[2]):
#     constants_table.append((token[2], "String value"))
#     continue
# if re.search(tokens.int_pattern.pattern, token[2]):
#     constants_table.append((token[2], "Int value"))
#     continue
