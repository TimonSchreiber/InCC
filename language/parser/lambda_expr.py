from .code_generation import gen
from .local_expr import *
from ..lexer.lambda_expr import tokens

used_procedures_and_classes |= {
    'LambdaExpression',
    'CallExpression'
}

precedence = [
    ['left', 'COMMA'],
    ['left', 'ARROW']
] + precedence

# List of arguments
def p_argument_list(p):
    '''expression_list : expression
                       | expression COMMA expression_list'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

def p_argument_list_ID(p):
    'expression_list : IDENTIFIER COMMA expression_list'
    p[0] = [gen().VariableExpression(p[1])] + p[3]

# List of parameters
def p_parameter_list(p):
    '''identifier_list : IDENTIFIER
                       | IDENTIFIER COMMA identifier_list'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

def p_expression_n_lambda(p):
    'expression : identifier_list ARROW expression'
    p[0] = gen().LambdaExpression(p[1], p[3])

def p_expression_0_lambda(p):
    'expression : ARROW expression'
    p[0] = gen().LambdaExpression([], p[2])

def p_expression_call_n_args(p):
    'expression : expression LPAREN expression_list RPAREN'
    p[0] = gen().CallExpression(p[1], p[3])

def p_expression_call_0_args(p):
    'expression : expression LPAREN RPAREN'
    p[0] = gen().CallExpression(p[1], [])
