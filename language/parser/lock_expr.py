from .code_generation import gen
from .ite_expr import *
from ..lexer.lock_expr import tokens

used_procedures_and_classes |= {
    'LockExpression'
}

precedence = [
    ['left', 'IN']
] + precedence

def p_identifier_list(p):
    '''identifier_list : IDENTIFIER
                       | IDENTIFIER COMMA identifier_list'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

def p_expression_lock(p):
    'expression : LOCK identifier_list IN expression'
    p[0] = gen().LockExpression(p[2], p[4])
