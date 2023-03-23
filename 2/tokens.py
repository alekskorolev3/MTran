import re

keywords = {
    'break': 'Break statement',
    'case': 'Case statement',
    'const': 'Constant identifier statement',
    'continue': 'Continue statement',
    'default': 'keyword',
    'do': 'Loop statement',
    'else': 'keyword',
    'for': 'Loop statement',
    'goto': 'keyword',
    'if': 'Condition statement',
    'return': 'Return statement',
    'sizeof': 'keyword',
    'struct': 'keyword',
    'switch': 'Switch statement',
    'unsigned': 'keyword',
    'while': 'Loop statement'
}

datatypes = {
    'bool': 'data type',
    'char': 'data type',
    'double': 'data type',
    'enum': 'data type',
    'float': 'data type',
    'int': 'data type',
    'long': 'data type',
    'short': 'data type',
    'string': 'data type',
}

operators = {
    '+': 'Arithmetic operator',
    '-': 'Arithmetic operator',
    '*': 'Arithmetic operator',
    '/': 'Arithmetic operator',
    '%': 'Arithmetic operator',
    '++': 'Arithmetic operator',
    '--': 'Arithmetic operator',
    '==': 'Relational operator',
    '!=': 'Relational operator',
    '<': 'Relational operator',
    '>': 'Relational operator',
    '<=': 'Relational operator',
    '>=': 'Relational operator',
    '&&': 'Logical operator',
    '||': 'Logical operator',
    '!': 'Logical operator',
    '=': 'Assigment operator',
    '+=': 'Assigment operator',
    '-=': 'Assigment operator',
    '*=': 'Assigment operator',
    '/=': 'Assigment operator',
    '%=': 'Assigment operator',
    '<<=': 'Assigment operator',
    '>>=': 'Assigment operator',
    '&=': 'Assigment operator',
    '^=': 'Assigment operator',
    '|=': 'Assigment operator',
}

separators = {
    '(': 'Separator',
    ')': 'Separator',
    '{': 'Separator',
    '}': 'Separator',
    '[': 'Separator',
    ']': 'Separator',
    ';': 'Separator',
    ',': 'Separator',
}

directives = {
    '#include': 'Directive statement',
    '#define': 'Directive statement',
    '#ifdef': 'Directive statement',
    '#ifndef': 'Directive statement',
    '#endif': 'Directive statement',
    '#undef': 'Directive statement',
    '#pragma': 'Directive statement',
}

functions = {
    'printf': 'Output function',
    'scanf': 'Input function'
}

keyword_pattern = re.compile('|'.join(list(keywords.keys())))
datatype_pattern = re.compile('|'.join(list(datatypes.keys())))
operators_pattern = re.compile('|'.join(re.escape(op) for op in operators))
separators_pattern = re.compile('|'.join(re.escape(op) for op in separators))
directives_pattern = re.compile('|'.join(list(directives.keys())))
functions_pattern = re.compile('|'.join(list(functions.keys())))

identifier_pattern = re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')
float_pattern = re.compile(r'\b\d+\.\d+\b')
int_pattern = re.compile(r'\b\d+\b')
string_pattern = re.compile(r'\".*?\"')
char_pattern = re.compile(r"'(?:\\.|[^\\'])*'")

pattern = re.compile(identifier_pattern.pattern + '|' + keyword_pattern.pattern + '|'
                          + datatype_pattern.pattern + '|'
                          + operators_pattern.pattern + '|'
                          + separators_pattern.pattern + '|'
                          + directives_pattern.pattern + '|'
                          + functions_pattern.pattern + '|'
                          + float_pattern.pattern + '|'
                          + int_pattern.pattern + '|'
                          + string_pattern.pattern + '|' + char_pattern.pattern)