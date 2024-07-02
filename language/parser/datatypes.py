from .code_generation import gen
from ..lexer.datatypes import tokens

used_procedures_and_classes = {
    'SelfEvaluatingExpression',
    'ListExpression',
    'ArrayExpression',
    'ArrayAccessExpression'
}

precedence = [[]]

def p_expression_single_value(p):
    '''expression : NUMBER
                  | FLOAT
                  | CHAR
                  | STRING'''
    p[0] = gen().SelfEvaluatingExpression(p[1])

def p_expression_list_non_empty(p):
    'expression : LIST LPAREN expression_list RPAREN'
    p[0] = gen().ListExpression(p[3])

def p_expression_list_empty(p):
    'expression : LIST LPAREN RPAREN'
    p[0] = gen().ListExpression(None)

def p_expression_array_non_empty(p):
    '''expression : LBRACKET expression_list RBRACKET
                  | ARRAY LPAREN expression_list RPAREN'''
    p[0] = gen().ArrayExpression(p[2]) if len(p) == 4 else gen().ArrayExpression(p[3])

def p_expression_array_empty(p):
    '''expression : LBRACKET RBRACKET
                  | ARRAY LPAREN RPAREN'''
    p[0] = gen().ArrayExpression([])

def p_expression_array_access(p):
    'expression : IDENTIFIER LBRACKET expression RBRACKET'
    p[0] = gen().ArrayAccessExpression(p[1], p[3])

def p_error(p):
    print(f'Syntax error at {p.value}')
