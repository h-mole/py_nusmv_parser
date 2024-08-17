import ply.lex as lex
from .models import Const

# 定义token
tokens = (
    "CASE",
    "ESAC",
    "ASSIGN",
    "COMMA",
    "BOOLEAN",
    "MODULE",
    "VAR",
    "DOTDOT",
    "IDENTIFIER",
    "INTEGER_NUMBER",
    "TRUE",
    "FALSE",
    "DOT",
    "LBRACKET",
    "RBRACKET",
    "LBRACE",
    "RBRACE",
    "LPAREN",
    "RPAREN",
    "SELF",
    "COLON",
    "SEMICOLON",
    "INIT_LOWERCASE",
    "NEXT_LOWERCASE",
    "ASSIGNMENT_SYMBOL",
    # operators
    "AND",
    "OR",
    "XOR",
    "EQUALS",
    "PLUS"
)


# 忽略空白字符
t_ignore = " \t\n"

reserved_words = {
    "A",
    "ABF",
    "ABG",
    "AF",
    "AG",
    "ASSIGN",
    "AX",
    "BU",
    "COMPASSION",
    "COMPUTE",
    "COMPWFF",
    "CONSTANTS",
    "CONSTRAINT",
    "CTLSPEC",
    "CTLWFF",
    "DEFINE",
    "E",
    "EBF",
    "EBG",
    "EF",
    "EG",
    "EX",
    "F",
    "FAIRNESS",
    "FALSE",
    "FROZENVAR",
    "G",
    "H",
    "IN",
    "INIT",
    "INVAR",
    "INVARSPEC",
    "ISA",
    "IVAR",
    "JUSTICE",
    "LTLSPEC",
    "LTLWFF",
    "MAX",
    "MDEFINE",
    "MIN",
    "MIRROR",
    "MODULE",
    "NAME",
    "O",
    "PRED",
    "PREDICATES",
    "PSLSPEC",
    "PSLWFF",
    "S",
    "SIMPWFF",
    "SPEC",
    "T",
    "TRANS",
    "TRUE",
    "U",
    "V",
    "VAR",
    "X",
    "Y",
    "Z",
    "abs",
    "array",
    "bool",
    "boolean",
    "case",
    "count",
    "esac",
    "extend",
    "in",
    "init",
    "integer",
    "max",
    "min",
    "mod",
    "next",
    "of",
    "process",
    "real",
    "resize",
    "self",
    "signed",
    "sizeof",
    "swconst",
    "union",
    "unsigned",
    "uwconst",
    "word",
    "word1",
    "xnor",
    "xor",
}

reserved_words_converter = {
    "TRUE": "TRUE",
    "FALSE": "FALSE",
    "self": "SELF",
    "MODULE": "MODULE",
    "VAR": "VAR",
    "boolean": "BOOLEAN",
    "ASSIGN": "ASSIGN",
    "init": "INIT_LOWERCASE",
    "next": "NEXT_LOWERCASE",
    "case": "CASE",
    "esac": "ESAC",
    
}
t_BOOLEAN = r"boolean"
t_CASE = r"case"
t_ESAC = r"esac"
t_XOR = r"xor"
t_ASSIGN = r"ASSIGN"
t_TRUE = r"TRUE"
t_FALSE = r"FALSE"
t_MODULE = r"MODULE"
t_INIT_LOWERCASE = r"init"
t_NEXT_LOWERCASE = r"next"
t_DOTDOT = r"\.\." # `..`符号
t_DOT = r"\."
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_COMMA = r","
t_ASSIGNMENT_SYMBOL = r":="

t_COLON = r":"
t_SEMICOLON = r";"
t_AND = r"&"
t_OR = r"&"
t_EQUALS = r"="
t_PLUS = r"\+"

def t_IDENTIFIER(t):
    r"[A-Za-z_][A-Za-z0-9_$#]*"
    t.value = t.value
    if t.value in reserved_words:
        t.type = reserved_words_converter[t.value]
    return t


# 定义规则
def t_INTEGER_NUMBER(t):
    r"-{0,1}[0-9]+"
    t.value = int(t.value)  # 将字符串转换为整数
    return t





# 错误处理
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# 构建lexer
lexer = lex.lex()


# 测试代码
def test_lexer(input_string):
    lexer.input(input_string)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


# 测试
test_lexer("""
MODULE Abc
           VAR a: BOOL;
""")
