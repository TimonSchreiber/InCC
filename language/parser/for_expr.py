from .code_generation import gen
from .loop_expr import *
from ..lexer.for_expr import tokens

used_procedures_and_classes |= {
    'ForExpression'
}

def p_expression_for(p):
    'expression : FOR expression SEPARATOR expression SEPARATOR expression DO expression'
    p[0] = gen().ForExpression(p[2], p[4], p[6], p[8])

'expression : FOR ID ASSIGN expression SEPARATOR expression boolean expression SEPARATOR ID ASSIGN expression DO expression'