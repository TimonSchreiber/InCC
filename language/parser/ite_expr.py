from .code_generation import gen
from .while_expr import *
from ..lexer.ite_expr import tokens

used_procedures_and_classes |= {
    'ITEExpression'
}

precedence = [
    ['left', 'THEN'],
    ['left', 'ELSE']
] + precedence

def p_expression_it(p):
    'expression : IF expression THEN expression'
    p[0] = gen().ITEExpression(p[2], p[4], None)

def p_expression_ite(p):
    'expression : IF expression THEN expression ELSE expression'
    p[0] = gen().ITEExpression(p[2], p[4], p[6])
