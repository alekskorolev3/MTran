from ply import yacc
from rules import tokens


class LALR1Parser:
    def __init__(self, text):
        self.text = text
        self.parser = yacc.yacc()

    def parse(self):
        tree = self.parser.parse(self.text)
        print(tree)


class Node:
    def parts_str(self):
        return "\n".join(map(str, [x for x in self.children]))

    def __init__(self, type, children):
        self.type = type
        self.children = children

    def __str__(self):
        return self.type + ":\n└───" + self.parts_str().replace("\n", "\n|\t")

    def add_parts(self, children):
        self.children += children
        return self


def p_program(p):
    """program : function"""
    p[0] = Node("program", p[1:])


def p_function(p):
    """function : func_header block"""

    p[0] = Node("function", p[1:])


def p_func_header(p):
    """func_header : DATA_TYPE FUNCDECL LPAR args RPAR"""
    p[0] = Node("func_declaration", [p[1], p[2], p[4]])


def p_args(p):
    """args :
    | expr
    | args COMMA expr"""
    if len(p) <= 2:
        p[0] = Node("args", p[1:] if p[1:] else ["EMPTY"])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_block(p):
    """block : LCURL body RCURL"""
    p[0] = Node("block", [p[2]])


def p_body(p):
    """body :
            | body line semicolons
            | body multiline"""
    if len(p) > 1:
        if p[1] is None:
            p[1] = Node("block_body", [])
        p[0] = p[1].add_parts([p[2]])
    else:
        p[0] = Node("block_body", [])


def p_semicolons(p):
    """semicolons : SEMICOLON
                  | semicolons SEMICOLON"""


def p_multiline(p):
    """multiline : if_statement
    | while_statement
    | for_statement"""
    p[0] = p[1]


def p_line(p):
    """line : modal_function
    | init
    | func
    | assign"""
    p[0] = p[1]


def p_modal_function(p):
    """modal_function : RETURN arg
    | BREAK
    | CONTINUE"""
    if len(p) == 3:
        p[0] = Node("modal_function", p[1:])
    else:
        p[0] = Node("modal_function", [p[1]])


def p_var_call(p):
    """var_cal : ID LCUADR expr RCUADR"""
    p[0] = Node("var_call", [p[1], p[3]])


def p_if_statement(p):
    """if_statement : IF LPAR condition RPAR block
    | if_statement ELSE block"""
    if len(p) == 4:
        p[0] = p[1].add_parts(["else", p[3]])
    else:
        p[0] = Node("if", [p[3], p[5]])


def p_while_statement(p):
    """while_statement : WHILE LPAR condition RPAR block"""
    p[0] = Node("while", [p[3], p[5]])


def p_for_statement(p):
    """for_statement : FOR LPAR assign SEMICOLON condition SEMICOLON change_val RPAR block"""
    p[0] = Node("for", [p[3], p[5], p[7], p[9]])


def p_change_value(p):
    """change_val : ID expr"""
    p[0] = Node("change_val", p[1:])


def p_condition(p):
    """condition : expr cond_sign expr"""
    p[0] = Node("condition", [p[1], p[2], p[3]])


def p_cond_sign(p):
    """cond_sign : DEQUAL
    | GT
    | LT
    | GE
    | LE
    | NOTEQUAL"""
    p[0] = p[1]


def p_init(p):
    """init :
    | DATA_TYPE ID SEMICOLON
    | DATA_TYPE ID EQUAL ID DIVMUL NUMBER
    | DATA_TYPE ID EQUAL expr
    | DATA_TYPE ID EQUAL var_cal
    | DATA_TYPE ID LCUADR RCUADR EQUAL array_init"""
    if len(p) > 5:
        p[0] = Node("init", [p[1], p[2], "[]", p[5], p[6]])
    else:
        p[0] = Node("init", p[1:])


def p_array_init(p):
    """array_init : LCURL init_block RCURL"""
    p[0] = Node("array_init", [p[2]])


def p_init_block(p):
    """init_block : arg
    | arg COMMA
    | init_block arg
    | init_block arg COMMA"""
    if len(p) == 2:
        p[0] = Node("init_block", p[1:])
    else:
        if p[2] != ",":
            p[0] = p[1].add_parts(p[2:])
        else:
            p[0] = Node("init_block", p[1:])


def p_assign(p):
    """assign : ID EQUAL expr
    | ID EQUAL var_cal
    | var_cal EQUAL expr
    | var_cal EQUAL var_cal
    | ID expr"""
    if len(p) == 5:
        p[0] = Node("assign", [p[2], p[4]])
    elif len(p) == 4 or len(p) == 3:
        p[0] = Node("assign", p[1:])
    else:
        p[0] = Node("assign", [p[1], p[3]])


def p_func(p):
    """func : CUSTOM_FUNC LPAR args RPAR
    | ID LPAR args RPAR
    | BUILD_IN LPAR args RPAR"""
    if len(p) == 3:
        p[0] = Node("func_call", [p[1], p[2]])
    else:
        p[0] = Node("func_call", [p[1], p[3]])


def p_expr(p):
    """expr : fact
    | PLUSMINUS PLUSMINUS
    | expr PLUSMINUS fact
    | expr MOD fact
    | ID PLUSMINUS ID
    | ID
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[2] == "+":
            p[0] = Node("increment", ["++"])
        elif p[2] == "-":
            p[0] = Node("decrement", ["--"])
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_fact(p):
    """fact : term
    | fact DIVMUL term"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])


def p_term(p):
    """term : arg
    | LPAR expr RPAR"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_arg(p):
    """arg : NUMBER
           | STRING
           | DATA_TYPE ID
           | DATA_TYPE ID LCUADR RCUADR
           | ID LCUADR RCUADR
           | var_cal
           | NUMBER ID
           | func"""
    if len(p) == 2:
        p[0] = Node("arg", [p[1]])
    else:
        p[0] = Node("arg", p[1:])


def p_error(p):
    raise SyntaxError(str(p.lineno) + ":" + str(p.lexpos) + " Error: unexpected token '" + str(p.value) + "'")