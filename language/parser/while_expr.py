from .code_generation import gen
from .for_expr import *
from ..lexer.while_expr import tokens

used_procedures_and_classes |= {
    'WhileExpression'
}

def p_expression_while(p):
    'expression : WHILE expression DO expression'
    p[0] = gen().WhileExpression(p[2], p[4])
