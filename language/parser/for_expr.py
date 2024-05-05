from .loop_expr import *
from ..lexer.for_expr import tokens, for_lexer
import interpreter.all_expr as all_expr

### the generator
# these items are expected to be implemented in module generate (see below)
used_procedures_and_classes |= {
    'ForExpression'
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

def p_expression_for(p):
    'expression : FOR assign_expr SEPARATOR bool_expr SEPARATOR assign_expr DO expression'
    p[0] = gen.ForExpression(p[2], p[4], p[6], p[8])

def p_expression_assign_expr(p):
    'assign_expr : IDENTIFIER ASSIGN expression'
    p[0] = gen.AssignmentExpression(p[1], p[3])

def p_expression_bool_expr(p):
    '''bool_expr : expression AND expression
                 | expression NAND expression
                 | expression OR expression
                 | expression NOR expression
                 | expression XOR expression
                 | expression EQ expression
                 | expression NEQ expression
                 | expression IMPL expression'''
    p[0] = gen.BinaryOperatorExpression(p[1], p[2], p[3])


### the REPL

set_generator_module(all_expr)
check_generator_module()

for_parser = yacc(start='expression')

# testing
if __name__ == '__main__':
    env = {}
    while True:
        i=input("repl > ")
        result = for_parser.parse(input=i, lexer=for_lexer)
        print(i,"\n\t",result.eval(env))
