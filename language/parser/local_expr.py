from .code_generation import gen
from .lock_expr import *
from ..lexer.local_expr import tokens

used_procedures_and_classes |= {
    'LocalExpression'
}

def p_expression_local(p):
    'expression : LOCAL IDENTIFIER ASSIGN expression IN expression'
    p[0] = gen().LocalExpression(p[2], p[4], p[6])
