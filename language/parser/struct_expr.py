from .code_generation import gen
from .lambda_expr import *
from ..lexer.struct_expr import tokens

used_procedures_and_classes |= {
    'StructExpression',
    'StructMemberAccessExpression',
    'StructExtendExpression'
}

precedence = precedence + [
    ['left', 'DOT']
]

def p_expression_struct(p):
    'expression : STRUCT BEGIN struct_body END'
    p[0] = gen().StructExpression(p[3])

def p_struct_body(p):
    '''struct_body : IDENTIFIER ASSIGN expression
                   | struct_body SEPARATOR IDENTIFIER ASSIGN expression'''
    p[0] = [(p[1], p[3])] if len(p) == 4 else p[1] + [(p[3], p[5])]

def p_expression_struct_member_access(p):
    'expression : IDENTIFIER dots IDENTIFIER'
    p[0] = gen().StructMemberAccessExpression(p[1], p[2], p[3])

def p_dot_notation(p):
    '''dots : DOT
            | dots DOT'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

def p_struct_extend_expression(p):
    'expression : EXTEND IDENTIFIER BEGIN struct_body END'
    p[0] = gen().StructExtendExpression(p[2], p[4])