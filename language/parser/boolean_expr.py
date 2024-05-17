from .code_generation import gen
from .assignment_expr import *
from ..lexer.boolean_expr import tokens

used_procedures_and_classes |= {
    'BooleanValueExpression'
}

# insert above 'ASSIGN' but below 'EQUALS'
precedence.insert(1, ['left', 'XOR', 'NEQ', 'EQ', 'IMPL'])
precedence.insert(1, ['left', 'AND', 'NAND'])
precedence.insert(1, ['left', 'OR', 'NOR'])

def p_expression_unary_not(p):
    '''expression : NOT expression %prec UMINUS'''
    p[0] = gen().UnaryOperatorExpression(p[1], p[2])

def p_expression_binary_boolean(p):
    '''expression : expression AND expression
                  | expression NAND expression
                  | expression OR expression
                  | expression NOR expression
                  | expression XOR expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression IMPL expression'''
    p[0] = gen().BinaryOperatorExpression(p[1], p[2], p[3])

def p_expression_boolean_value(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = gen().BooleanValueExpression(p[1])
