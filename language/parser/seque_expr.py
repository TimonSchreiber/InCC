from .bool_expr import *
from ..lexer.seque_expr import tokens, seque_lexer
import interpreter.all_expr as all_expr

### the generator
# these items are expected to be implemented in module generate (see below)
used_procedures_and_classes |= {
    'SequenceExpression'
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
precedence = precedence


def p_expression_sequence(p):
    'expression : BEGIN body END'
    p[0] = gen.SequenceExpression(p[2])

def p_bodyn(p):
    '''body : expression
            | body SEPARATOR expression'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]


### the REPL

set_generator_module(all_expr)
check_generator_module()

seque_parser = yacc(start='expression')

# testing
if __name__ == '__main__':
    env = {}
    while True:
        i=input("repl > ")
        result = seque_parser.parse(input=i, lexer=seque_lexer)
        print(i,"\n\t",result.eval(env))
