import ply.yacc as yacc
from .lexer import lexer
from .lexer import tokens
from .models import *


# """
# module :: MODULE identifier [( module_parameters )] [module_body]
# module_parameters ::
# identifier
# | module_parameters , identifier
# module_body ::
# module_element
# | module_body module_element
# module_element ::
# var_declaration
# | ivar_declaration
# | frozenvar_declaration
# | define_declaration
# | constants_declaration
# | assign_constraint
# | trans_constraint
# | init_constraint
# | invar_constraint
# | fairness_constraint
# | ctl_specification
# | invar_specification
# | ltl_specification
# | compute_specification
# | isa_declaration
# """
def p_module(p):
    """
    module : MODULE identifier module_body
    """
    if len(p) == 4:
        p[0] = Module(p[2], p[3])
    else:
        # p[0] = Module(p[2], [])
        raise NotImplementedError("Module without body")


def p_module_body(p):
    """
    module_body : module_element
        | module_body module_element
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


# module_element :: var_declaration
# | ivar_declaration
# | frozenvar_declaration
# | define_declaration
# | constants_declaration
# | assign_constraint
# | trans_constraint
# | init_constraint
# | invar_constraint
# | fairness_constraint
# | ctl_specification
# | invar_specification
# | ltl_specification
# | compute_specification
# | isa_declaration
def p_module_element(p):
    """
    module_element : var_declaration
        | assign_constraint
    """
    p[0] = p[1]


# assign_constraint :: ASSIGN assign_list
def p_assign_constraint(p):
    """
    assign_constraint : ASSIGN assign_list
    """
    p[0] = AssignConstraint(p[2])


# assign_list :: assign ;
# | assign_list assign ;


def p_assign_list(p):
    """
    assign_list : assign SEMICOLON
        | assign_list assign SEMICOLON
    """
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


# assign ::
# complex_identifier := simple_expr
# | init ( complex_identifier ) := simple_expr
# | next ( complex_identifier ) := next_expr
def p_assign(p):
    """
    assign : complex_identifier ASSIGNMENT_SYMBOL simple_expr
        | INIT_LOWERCASE LPAREN complex_identifier RPAREN ASSIGNMENT_SYMBOL simple_expr
        | NEXT_LOWERCASE LPAREN complex_identifier RPAREN ASSIGNMENT_SYMBOL next_expr
    """
    match p[1:]:
        case [complex_identifier, _, simple_expr]:
            p[0] = Assign(complex_identifier, simple_expr)
        case ["init", "(", complex_identifier, ")", ":=", simple_expr]:
            p[0] = Assign(complex_identifier, simple_expr, "init")
        case ["next", "(", complex_identifier, ")", ":=", next_expr]:
            p[0] = Assign(complex_identifier, next_expr, "next")
        case _:
            raise NotImplementedError(p[:])
    # p[0] = Assign(p[1], p[3])


# var_declaration :: VAR var_list
# var_list :: identifier : type_specifier ;
# | var_list identifier : type_specifier ;
def p_var_declaration(p):
    """
    var_declaration : VAR var_list
    """
    p[0] = VarDeclaration(p[2])


def p_var_list(p):
    """
    var_list : identifier COLON type_specifier SEMICOLON
        | var_list identifier COLON type_specifier SEMICOLON
    """
    # p[0] = VarDeclaration(p[2])
    match p[1:]:
        case [identifier, ":", type_specifier, ";"]:
            p[0] = [VarDeclItem(identifier, type_specifier)]
        case [var_list, identifier, ":", type_specifier, ";"]:
            p[0] = var_list + [VarDeclItem(identifier, type_specifier)]
        case _:
            raise NotImplementedError(p[1:])


def p_type_specifier(p):
    """
    type_specifier : simple_type_specifier
        | module_type_specifier
    """
    p[0] = p[1]


# simple_type_specifier ::
#   boolean
#       | word [ basic_expr ]
#       | unsigned word [ basic_expr ]
#       | signed word [ basic_expr ]
#       | { enumeration_type_body }
#       | basic_expr .. basic_expr
#       | array basic_expr .. basic_expr of simple_type_specifier
def p_simple_type_specifier(p):
    """
    simple_type_specifier : BOOLEAN
        | LBRACE enumeration_type_body RBRACE
    """
    match p[1:]:
        case ["boolean"]:
            p[0] = BooleanType()
        case ["{", enumeration_type_body, "}"]:
            p[0] = EnumerationType(enumeration_type_body)
        case _:
            raise NotImplementedError(p[1:])


# enumeration_type_body :: enumeration_type_value
#   | enumeration_type_body , enumeration_type_value
def p_enumeration_type_body(p):
    """
    enumeration_type_body : enumeration_type_value
        | enumeration_type_body COMMA enumeration_type_value
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# enumeration_type_value :: symbolic_constant
#   | integer_number
def p_enumeration_type_value(p):
    """
    enumeration_type_value : symbolic_constant
        | integer_constant
    """
    p[0] = EnumerationTypeValue(p[1])


# module_type_specifier ::
# | identifier [ ( [ parameter_list ] ) ]
# | process identifier [ ( [ parameter_list ] ) ]
def p_module_type_specifier(p):
    """
    module_type_specifier : identifier LPAREN parameter_list RPAREN
    """
    p[0] = ModuleType(p[1], p[3])


# parameter_list ::
# simple_expr
# | parameter_list , simple_expr


def p_parameter_list(p):
    """
    parameter_list : simple_expr
        | parameter_list COMMA simple_expr
    """
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]


# next_expr :: basic_expr
def p_next_expr(p):
    """
    next_expr : basic_expr
    """
    p[0] = p[1]


def p_simple_expr(p):
    """
    simple_expr : basic_expr
    """
    p[0] = p[1]


# basic_expr ::
#  constant
#  | variable_identifier
#  | define_identifier
#  | ( basic_expr )
#  | ! basic_expr
#  | abs ( basic_expr )
#  | max ( basic_expr )
#  | min ( basic_expr )
#  | basic_expr & basic_expr
#  | basic_expr | basic_expr
#  | basic_expr xor basic_expr
#  | basic_expr xnor basic_expr
#  | basic_expr-> basic_expr
#  | basic_expr <-> basic_expr
#  | basic_expr = basic_expr
#  | basic_expr != basic_expr
#  | basic_expr < basic_expr
#  | basic_expr > basic_expr
#  | basic_expr <= basic_expr
#  | basic_expr >= basic_expr
#  | - basic_expr
#  | basic_expr + basic_expr
#  | basic_expr - basic_expr
#  | basic_expr * basic_expr
#  | basic_expr / basic_expr
#  | basic_expr mod basic_expr
#  | basic_expr >> basic_expr
#  | basic_expr << basic_expr
#  | basic_expr [ index ]
#  | basic_expr [ basic_expr : basic_expr ]
#  | basic_expr :: basic_expr
#  | word1 ( basic_expr )
#  | bool ( basic_expr )
#  | toint ( basic_expr )
#  | count ( basic_expr_list )
#  | swconst ( basic_expr , basic_expr )
#  | uwconst ( basic_expr, basic_expr )
#  | signed ( basic_expr )
#  | unsigned ( basic_expr )
#  | sizeof ( basic_expr )
#  | extend ( basic_expr , basic_expr)
#  | resize ( basic_expr , basic_expr)
#  | basic_expr union basic_expr
#  | { set_body_expr }
#  | basic_expr .. basic_expr
#  | basic_expr in basic_expr
#  | basic_expr ? basic_expr : basic_expr
#  | case_expr
#  | basic_next_expr
def p_basic_expr(p):
    """
    basic_expr : case_expr
        | LBRACE set_body_expr RBRACE
        | binop_level_6
    """

    match p[1:]:
        case [Const]:
            assert p[1] is not None
            p[0] = p[1]
        case [expr_left, "+" | "-" | "=" | "!=" | "&", expr_right]:
            p[0] = BinaryOperator(expr_left, p[2], expr_right)
        case ["{", set_body_expr, "}"]:
            p[0] = SetExpr(set_body_expr)
        case _:
            raise NotImplementedError(p[:])

def p_binop_level_6(p):
    """
    binop_level_6 : binop_level_5
        | binop_level_5 AND binop_level_6
        | binop_level_5 OR binop_level_6
        | binop_level_5 XOR binop_level_6
    """
    match p[1:]:
        case [expr]:
            p[0] = expr
        case [expr_left, op, expr_right]:
            p[0] = BinaryOperator(expr_left, op, expr_right)
        case _:
            raise NotImplementedError(p[:])




def p_binop_level_5(p):
    """
    binop_level_5 : bin_op_lv4
        | bin_op_lv4 EQUALS binop_level_5
    """
    match p[1:]:
        case [expr]:
            p[0] = expr
        case [expr_left, op, expr_right]:
            p[0] = BinaryOperator(expr_left, op, expr_right)
        case _:
            raise NotImplementedError(p[:])

def p_binop_level_4(p):
    """
    bin_op_lv4 : sub_basic_expr PLUS bin_op_lv4
        | sub_basic_expr
    """
    match p[:]:
        case [_, expr, op, expr2]:
            p[0] = BinaryOperator(expr, op, expr2)
        case [_, expr]:
            p[0] = expr
        case _:
            raise NotImplementedError(p[:])
    # p [0] = BinaryOperator(p[1], p[2], p[3])

def p_sub_basic_expr(p):
    """
    sub_basic_expr :  LPAREN basic_expr RPAREN
        | constant
        | variable_identifier
        | define_identifier
    """
    match p[:]:
        case [_, "(", expr, ")"]:
            p[0] = expr
        case [_, expr]:
            p[0] = expr
        case _:
            raise NotImplementedError(p[:])

# case_expr :: case case_body esac
def p_case_expr(p):
    """
    case_expr : CASE case_body ESAC
    """
    p[0] = CaseExpr(p[2])


# case_body :: basic_expr : basic_expr ;
#   | case_body basic_expr : basic_expr ;
def p_case_body(p):
    """
    case_body : basic_expr COLON basic_expr SEMICOLON
        | case_body basic_expr COLON basic_expr SEMICOLON
    """
    match p[1:]:
        case [basic_expr_1, ':', basic_expr_2, ';']:
            p[0] = [CaseBodyItem(basic_expr_1, basic_expr_2)]
        case [case_body, basic_expr_1, ':', basic_expr_2, ';']:
            p[0] = case_body + [CaseBodyItem(basic_expr_1, basic_expr_2)]
        case _:
            raise NotImplementedError(p[:])

# set_body_expr :: basic_expr
#   | set_body_expr , basic_expr
def p_set_body_expr(p):
    """
    set_body_expr : basic_expr
        | set_body_expr COMMA basic_expr
    """
    match p[1:]:
        case [basic_expr]:
            p[0] = [basic_expr]
        case [set_body_expr, COMMA, basic_expr]:
            p[0] = set_body_expr + [basic_expr]


# Grammar rules
def p_constant(p):
    """
    constant : boolean_constant
        | integer_constant
        | symbolic_constant
        | range_constant
    """
    # TODO missing: word_constant

    p[0] = p[1]  # The result is the value of the constant


def p_complex_identifier(p):
    """
    complex_identifier : IDENTIFIER
        | complex_identifier DOT IDENTIFIER
        | complex_identifier LBRACKET simple_expr RBRACKET
        | SELF
    """
    match p[1:]:
        case [str()]:
            p[0] = Identifier(p[1])
        case [Expr(), ".", identifier]:
            p[0] = ComplexIdentifier(p[1], identifier, "field")
        case [Expr(), "[", simple_expr, "]"]:
            p[0] = ComplexIdentifier(p[1], simple_expr, "index")
        case _:
            raise NotImplementedError(p[:])
    

def p_variable_identifier(p):
    """
    variable_identifier : complex_identifier
    """
    p[0] = p[1]


def p_identifier(p):
    """
    identifier : IDENTIFIER
    """
    p[0] = Identifier(p[1])


def p_define_identifier(p):
    """
    define_identifier : complex_identifier
    """
    p[0] = p[1]


# def p_symbolic_


def p_symbolic_constant(p):
    """
    symbolic_constant : IDENTIFIER
    """
    p[0] = Const(p[1], "symbolic")


def p_integer_constant(p):
    """
    integer_constant : INTEGER_NUMBER
    """
    p[0] = Const(int(p[1]), "integer")


def p_boolean_constant(p):
    """
    boolean_constant : TRUE
                     | FALSE
    """
    p[0] = Const(True if p[1] == "TRUE" else False, "boolean")


def p_range_constant(p):
    """
    range_constant : INTEGER_NUMBER DOTDOT INTEGER_NUMBER
    """
    p[0] = Const((int(p[1]), int(p[3])), "range")


def p_error(p):
    print(p.lineno)
    print(f"Syntax error at '{p.value}'")


parser = yacc.yacc(debug=True)

def parse_nusmv_string(input_string: str):
    return parser.parse(input_string)