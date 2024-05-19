from .code_generation import gen
from .local_expr import *
from ..lexer.lambda_expr import tokens

used_procedures_and_classes |= {
    'LambdaExpression',
    'CallExpression'
}

# precedence = [
#     ['left', 'ARROW']
# ] + precedence

def p_expression_lambda(p):
    'expression : IDENTIFIER ARROW expression'
    p[0] = gen().LambdaExpression(p[1], p[3])

def p_expression_call(p):
    'expression : expression LPAREN expression RPAREN'
    p[0] = gen().CallExpression(p[1], p[3])
