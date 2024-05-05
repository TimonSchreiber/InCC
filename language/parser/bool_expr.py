from .comp_expr import *
from ..lexer.bool_expr import tokens, bool_lexer
import interpreter.all_expr as all_expr

### the generator
# these items are expected to be implemented in module generate (see below)
used_procedures_and_classes |= {
    'BooleanValueExpression'
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
    ['left', 'OR', 'NOR'],
    ['left', 'AND', 'NAND'],
    ['left', 'XOR', 'IMPL'],
] + precedence


def p_expression_unary_not(p):
    '''expression : NOT expression %prec UMINUS'''
    p[0] = gen.UnaryOperatorExpression(p[1], p[2])

def p_expression_binary_boolean(p):
    '''expression : expression AND expression
                  | expression NAND expression
                  | expression OR expression
                  | expression NOR expression
                  | expression EQ expression %prec EQUALS
                  | expression XOR expression
                  | expression IMPL expression'''
    p[0] = gen.BinaryOperatorExpression(p[1], p[2], p[3])

def p_expression_boolean_value(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = gen.BooleanValueExpression(p[1])


### the REPL

set_generator_module(all_expr)
check_generator_module()

bool_parser = yacc(start='expression')

# testing
if __name__ == '__main__':
    env = {}
    while True:
        i=input("repl > ")
        result = bool_parser.parse(input=i, lexer=bool_lexer)
        print(i,"\n\t",result.eval(env))
