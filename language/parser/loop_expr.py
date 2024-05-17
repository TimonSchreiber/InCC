from .code_generation import gen
from .sequence_expr import *
from ..lexer.loop_expr import tokens

used_procedures_and_classes |= {
    'LoopExpression'
}

precedence = [
    ['left', 'DO']
] + precedence

def p_expression_loop(p):
    'expression : LOOP expression DO expression'
    p[0] = gen().LoopExpression(p[2], p[4])
