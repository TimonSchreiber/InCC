from .code_generation import gen
from .arithmetic_expr import *
from ..lexer.comparison_expr import tokens

precedence = [
    ['left', 'EQUALS', 'NOT_EQUALS'],
    ['left', 'LESS_THEN', 'GREATER_THEN', 'LESS_EQUALS', 'GREATER_EQUALS']
] + precedence

def p_expression_binary_comparison(p):
    '''expression : expression LESS_THEN expression
                  | expression GREATER_THEN expression
                  | expression LESS_EQUALS expression
                  | expression GREATER_EQUALS expression
                  | expression EQUALS expression
                  | expression NOT_EQUALS expression'''
    p[0] = gen().BinaryOperatorExpression(p[1], p[2], p[3])
