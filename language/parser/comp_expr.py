from .arith_expr import *
from ..lexer.comp_expr import tokens, comp_lexer
import interpreter.all_expr as all_expr

### the generator
# these items are expected to be implemented in module generate (see below)
used_procedures_and_classes = used_procedures_and_classes

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
    ['left', 'LESS_THEN', 'GREATER_THEN', 'LESS_EQUALS', 'GREATER_EQUALS'],
    ['left', 'EQUALS', 'NOT_EQUALS']
] + precedence

def p_expression_binary_comparison(p):
    '''expression : expression LESS_THEN expression
                  | expression GREATER_THEN expression
                  | expression LESS_EQUALS expression
                  | expression GREATER_EQUALS expression
                  | expression EQUALS expression
                  | expression NOT_EQUALS expression'''
    p[0] = gen.BinaryOperatorExpression(p[1], p[2], p[3])


### the REPL

set_generator_module(all_expr)
check_generator_module()

comp_parser = yacc(start='expression')

# testing
if __name__ == '__main__':
    env = {}
    while True:
        i=input("repl > ")
        result = comp_parser.parse(input=i, lexer=comp_lexer)
        print(i,"\n\t",result.eval(env))
