import re
import prettytable
import tokens


def extract_tokens(text):
    l = []

    for index, line in enumerate(text.splitlines()):
        for match in re.finditer(tokens.pattern, line):
            l.append((index, match.start(), match.group()))

    return l


with open('/Users/artem/PycharmProjects/MTran/second/2/test.c', 'r') as f:
    text = f.read()

identifiers_table = prettytable.PrettyTable()
constants_table = prettytable.PrettyTable()
keywords_table = prettytable.PrettyTable()
datatypes_table = prettytable.PrettyTable()
operators_table = prettytable.PrettyTable()
directives_table = prettytable.PrettyTable()
functions_table = prettytable.PrettyTable()

identifiers_table.title = 'IDENTIFIERS TABLE'
identifiers_table.field_names = ['TOKEN', 'DESCRIPTION']

constants_table.title = 'CONSTANTS TABLE'
constants_table.field_names = ['TOKEN', 'DESCRIPTION']

keywords_table.title = 'KEY WORDS TABLE'
keywords_table.field_names = ['TOKEN', 'DESCRIPTION']

datatypes_table.title = 'DATA TYPES TABLE'
datatypes_table.field_names = ['TOKEN', 'DESCRIPTION']

operators_table.title = 'OPERATORS TABLE'
operators_table.field_names = ['TOKEN', 'DESCRIPTION']

directives_table.title = 'DIRECTIVES TABLE'
directives_table.field_names = ['TOKEN', 'DESCRIPTION']

functions_table.title = 'FUNCTIONS TABLE'
functions_table.field_names = ['TOKEN', 'DESCRIPTION']

set_of_tokens = extract_tokens(text)

_ident = []
_err = []
_func = False
_brackets = []

for i, token in enumerate(set_of_tokens):

    if token[2] == "{":
        _brackets.append(token)
    elif token[2] == "}":
        if len(_brackets) == 0:
            raise SyntaxError(str(token[0] + 1) + ":" + str(token[1]) + " Error: Unmatched closing bracket at token: '" + str(token[2]) + "'")
        else:
            _brackets.pop()

    if i + 1 < set_of_tokens.__len__():
        if token[0] < set_of_tokens[i + 1][0]:
            if not (token[2] in tokens.closing) and not (token[2] in tokens.opened):
                if (set_of_tokens[i + 1][2] in tokens.keywords) \
                        or (set_of_tokens[i + 1][2] in tokens.datatypes) \
                        or (set_of_tokens[i + 1][2] in tokens.closing) or (set_of_tokens[i + 1][2] in _ident):
                    raise SyntaxError( str(token[0] + 1) + ":" + str(token[1]) + " Error: Missing semicolon")

    if token[2] in tokens.keywords:
        if set_of_tokens[i - 1][2] not in tokens.datatypes:
            keywords_table.add_row([token[2], tokens.keywords[token[2]]])
            continue
        else:
            raise SyntaxError(str(token[0] + 1) + ":" + str(token[1]) + " Error: Expected unqualified-id before '" + str(token[2]) + "'")

    if token[2] in tokens.datatypes:
        datatypes_table.add_row([token[2], tokens.datatypes[token[2]]])
        continue
    if token[2] in tokens.functions:
        functions_table.add_row([token[2], tokens.functions[token[2]]])
        continue
    if token[2] in directives_table:
        directives_table.add_row([token[2], tokens.directives[token[2]]])
        continue

    if set_of_tokens[i - 1][2] == ")":
        _func = False

    if re.search(tokens.string_pattern.pattern, token[2]):
        if set_of_tokens[i - 1][2] in tokens.operators:
            constants_table.add_row([token[2], "Constant of string type"])
            continue
        elif _func:
            constants_table.add_row([token[2], "Constant of string type"])
            continue
        elif set_of_tokens[i - 1][2] == "return":
            constants_table.add_row([token[2], "Constant of string type"])
            continue
        else:
            raise SyntaxError(
                str(token[0] + 1) + ":" + str(token[1]) + " Error: Expected identifier before constant")

    if re.search(tokens.char_pattern.pattern, token[2]):
        if set_of_tokens[i - 1][2] in tokens.operators:
            constants_table.add_row([token[2], "Constant of char type"])
            continue
        elif _func:
            constants_table.add_row([token[2], "Constant of char type"])
            continue
        elif set_of_tokens[i - 1][2] == "return":
            constants_table.add_row([token[2], "Constant of char type"])
            continue
        else:
            raise SyntaxError(
                str(token[0] + 1) + ":" + str(token[1]) + " Error: Expected identifier before constant")

    if re.search(tokens.identifier_pattern.pattern, token[2]):
        if token[2] not in _ident:
            if set_of_tokens[i + 1][2] == "(":
                _func = True
                functions_table.add_row([token[2], "Function"])
            elif set_of_tokens[i - 1][2] in tokens.datatypes:
                _ident.append(token[2])
                identifiers_table.add_row([token[2], "Identifier of " + str(tokens.datatypes[set_of_tokens[i - 1][2]])])
                continue
            else:
                raise SyntaxError(str(token[0] + 1) + ":" + str(token[1]) + " Error: '" + str(token[2]) + "' was not declared in this scope")
        else:
            if set_of_tokens[i - 1][2] in tokens.datatypes:
                raise SyntaxError(str(token[0] + 1) + ":" + str(token[1]) + " Error: redeclaration of '" + str(token[2]) + "'")

    if token[2] in tokens.operators:
        if token[2] == '++':
            if set_of_tokens[i - 1][2] in _ident or set_of_tokens[i + 1][2] in _ident:
                operators_table.add_row([token[2], tokens.operators[token[2]]])
                continue
            else:
                raise SyntaxError(
                    str(token[0] + 1) + ":" + str(token[1]) + " Expected identifier before '" + str(token[2]) + "' token")

        if not set_of_tokens[i - 1][2] in _ident:
            raise SyntaxError(
                str(token[0] + 1) + ":" + str(token[1]) + " Expected identifier before '" + str(token[2]) + "' token")
        else:
            operators_table.add_row([token[2], tokens.operators[token[2]]])
            continue

    if re.search(tokens.float_pattern.pattern, token[2]):
        if set_of_tokens[i - 1][2] in tokens.operators:
            constants_table.add_row([token[2], "Constant of float type"])
            continue
        elif _func:
            constants_table.add_row([token[2], "Constant of float type"])
            continue
        elif set_of_tokens[i - 1][2] == "return":
            constants_table.add_row([token[2], "Constant of float type"])
            continue
        else:
            raise SyntaxError(
                str(token[0] + 1) + ":" + str(token[1]) + " Error: Expected identifier before constant")

    if re.search(tokens.int_pattern.pattern, token[2]):
        if set_of_tokens[i - 1][2] in tokens.operators:
            constants_table.add_row([token[2], "Constant of int type"])
            continue
        elif _func:
            constants_table.add_row([token[2], "Constant of int type"])
            continue
        elif set_of_tokens[i - 1][2] == "return":
            constants_table.add_row([token[2], "Constant of int type"])
            continue
        else:
            raise SyntaxError(
                str(token[0] + 1) + ":" + str(token[1]) + " Error: Expected identifier before constant")


_last = set_of_tokens[-1]

if len(_brackets) != 0:
    raise SyntaxError(str(_brackets[-1][0] + 1) + ":" + str(_brackets[-1][1]) + " Error: Unmatched opening bracket at token: '" + str(_brackets[-1][2]) + "'")
if not _last[2].endswith((';', '}')):
    raise SyntaxError("Missing semicolon at the end of token:" + str(_last[0]) + " " + str(_last[1]))

print(identifiers_table)
print(constants_table)
print(keywords_table)
print(functions_table)
print(datatypes_table)
print(operators_table)
print(directives_table)
