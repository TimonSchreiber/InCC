# from ply.yacc import yacc
# from ply.lex import lex
from ..lexer.arith_expr import tokens#, arith_lexer
import interpreter.all_expr as all_expr

### the generator
# these items are expected to be implemented in module generate (see below)
used_procedures_and_classes = {
    'SelfEvaluatingExpression',
    'BinaryOperatorExpression',
    'UnaryOperatorExpression',
    'ParenthesisExpression'
}


gen = None

def set_generator_module(m):
    global gen
    gen = m

def generator_module_implements(used_procedures_and_classes): # check availability of module and all referenced items
    return all(hasattr(gen, x) for x in used_procedures_and_classes)

def check_generator_module():
    if not gen:
        raise Exception("No code generator provided please use 'set_generator_module()' in parser module")
    if not generator_module_implements(used_procedures_and_classes):
        raise Exception("code generator doesn't implement all expected functions")

### the parser

precedence = [
    ['left', 'PLUS', 'MINUS'],
    ['left', 'TIMES', 'DIVIDE'],
    ['right', 'UMINUS']
]


def p_expression_number(p):
    '''expression : NUMBER
                  | FLOAT'''
    p[0] = gen.SelfEvaluatingExpression(p[1])

def p_expression_unary_minus(p):
    '''expression : MINUS expression %prec UMINUS'''
    p[0] = gen.UnaryOperatorExpression(p[1], p[2])

def p_expression_binary_arithmetic(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = gen.BinaryOperatorExpression(p[1], p[2], p[3])

def p_expression_parenthesis(p):
    'expression : LPAREN expression RPAREN'
    p[0] = gen.ParenthesisExpression(p[2])


def p_error(p):
    print("Syntax error in input!")


### the REPL

set_generator_module(all_expr)
check_generator_module()


# testing
# if __name__ == '__main__':
#     from ply.yacc import yacc
#     arith_parser = yacc(start='expression')
#     env = {}
#     while True:
#         i=input("repl > ")
#         result = arith_parser.parse(input=i, lexer=lex())
#         print(i,"\n\t",result.eval(env))
