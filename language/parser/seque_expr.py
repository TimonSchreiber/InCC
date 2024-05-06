from .code_generation import gen
from .bool_expr import *
from ..lexer.seque_expr import tokens

used_procedures_and_classes |= {
    'SequenceExpression'
}

precedence = precedence + [
    ['left', 'SEPARATOR']
]

def p_expression_sequence(p):
    'expression : BEGIN body END'
    p[0] = gen().SequenceExpression(p[2])

def p_bodyn(p):
    '''body : expression
            | body SEPARATOR expression'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]
