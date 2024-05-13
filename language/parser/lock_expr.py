from .code_generation import gen
from .ite_expr import *
from ..lexer.lock_expr import tokens

used_procedures_and_classes |= {
    'LockExpression'
}

precedence = [
    ['left', 'IN']
] + precedence

def p_expression_lock(p):
    'expression : LOCK IDENTIFIER IN expression'
    p[0] = gen().LockExpression(p[2], p[4])
