from ply.lex import TOKEN

tokens = (
    "FUNCDECL",
    "LPAR",
    "RPAR",
    "COMMA",
    "LCURL",
    "RCURL",
    "LCUADR",
    "RCUADR",
    "CUSTOM_FUNC",
    "EQUAL",
    "SEMICOLON",
    "NUMBER",
    "DATA_TYPE",
    "ID",
    "BUILD_IN",
    "PLUSMINUS",
    "DIVMUL",
    "STRING",
    "IF",
    "ELSE",
    "DEQUAL",
    "RETURN",
    "GT",
    "LT",
    "GE",
    "LE",
    "MOD",
    "NOTEQUAL",
    "WHILE",
    "FOR",
    "CONTINUE",
    "BREAK",
    "DO"
)

identifier = r"[a-zA-Z]\w*"

types = {
    "int": "DATA_TYPE",
    "float": "DATA_TYPE",
    "double": "DATA_TYPE",
    "char": "DATA_TYPE",
    "void": "DATA_TYPE",
    "string": "DATA_TYPE"
}

reserved = {
    "if": "IF",
    "else": "ELSE",
    "auto": "DATA_TYPE",
    "while": "WHILE",
    "for": "FOR",
    "do": "DO",
    "break": "BREAK",
    "continue": "CONTINUE",
    "return": "RETURN",
    "sizeof": "BUILD_IN",
    "printf": "BUILD_IN",
    "scanf": "BUILD_IN",
}

t_LCUADR = r"\["
t_RCUADR = r"\]"
t_LPAR = r"\("
t_RPAR = r"\)"
t_COMMA = r","
t_LCURL = r"\{"
t_RCURL = r"\}"
t_DEQUAL = r"\=\="
t_GE = r"\>\="
t_LE = r"\<\="
t_GT = r"\>"
t_LT = r"\<"
t_MOD = r"\%"
t_NOTEQUAL = r"!\="
t_EQUAL = r"\="
t_SEMICOLON = r";"
t_PLUSMINUS = r"\+|\-"
t_DIVMUL = r"/|\*"
t_STRING = r'("(\\.|[^"])*")|(\'(\\.|[^\'])*\')'


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_NUMBER(t):
    r"[0-9.]+"
    try:
        t.value = int(t.value)
    except BaseException:
        try:
            t.value = float(t.value)
        except BaseException:
            t.value = None
    return t


class TypeDefine:
    type_define = False


@TOKEN(identifier)
def t_ID(t):
    if TypeDefine.type_define:
        TypeDefine.type_define = False
        if t.lexer.lexdata[t.lexpos + len(t.value)] == "(":
            reserved[t.value] = "CUSTOM_FUNC"
            t.type = "FUNCDECL"
        else:
            t.type = "ID"
    else:
        if t.lexer.lexdata[t.lexpos + len(t.value)] == "(":
            if (value := reserved.get(t.value, None)) is None:
                print("error")
            else:
                t.type = value
        else:
            if (res := types.get(t.value, "ID")) == "DATA_TYPE":
                TypeDefine.type_define = True

            t.type = res if t.value not in reserved else reserved[t.value]

    return t


def t_error(t):
    # print("Illegal character '%s' at line %d" % (t.value[0], t.lineno))
    t.lexer.skip(1)