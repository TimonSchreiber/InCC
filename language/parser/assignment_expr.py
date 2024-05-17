from .code_generation import gen
from .comparison_expr import *
from ..lexer.assignment_expr import tokens

used_procedures_and_classes |= {
    'VariableExpression',
    'AssignmentExpression'
}

precedence = [
    ['right', 'ASSIGN']
] + precedence

def p_expression_id(p):
    'expression : IDENTIFIER'
    p[0] = gen().VariableExpression(p[1])

def p_expression_assign(p):
    'expression : IDENTIFIER ASSIGN expression'
    p[0] = gen().AssignmentExpression(p[1], p[3])
