from .code_generation import gen
from .ite_expr import *
from ..lexer.lock_expr import tokens

used_procedures_and_classes |= {
    'LockExpression'
}

precedence = [
    ['left', 'IN']
] + precedence

# Using the identifier_list form lambda_expr.py to lock more than one variable
def p_expression_lock(p):
    'expression : LOCK identifier_list IN expression'
    p[0] = gen().LockExpression(p[2], p[4])
