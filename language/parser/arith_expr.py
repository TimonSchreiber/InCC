from .code_generation import gen
from ..lexer.arith_expr import tokens

used_procedures_and_classes = {
    'SelfEvaluatingExpression',
    'BinaryOperatorExpression',
    'UnaryOperatorExpression',
    'ParenthesisExpression'
}

precedence = [
    ['left', 'PLUS', 'MINUS'],
    ['left', 'TIMES', 'DIVIDE'],
    ['right', 'UMINUS']
]

def p_expression_number(p):
    '''expression : NUMBER
                  | FLOAT'''
    p[0] = gen().SelfEvaluatingExpression(p[1])

def p_expression_unary_minus(p):
    '''expression : MINUS expression %prec UMINUS'''
    p[0] = gen().UnaryOperatorExpression(p[1], p[2])

def p_expression_binary_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = gen().BinaryOperatorExpression(p[1], p[2], p[3])

def p_expression_parenthesis(p):
    'expression : LPAREN expression RPAREN'
    p[0] = gen().ParenthesisExpression(p[2])


def p_error(p):
    print("Syntax error in input!")
