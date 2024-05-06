from .seque_expr import *
from ..lexer.loop_expr import tokens#, loop_lexer
import interpreter.all_expr as all_expr

### the generator
# these items are expected to be implemented in module generate (see below)
used_procedures_and_classes |= {
    'LoopExpression'
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
    ['left', 'DO']
] + precedence


def p_expression_loop(p):
    'expression : LOOP expression DO expression'
    p[0] = gen.LoopExpression(p[2], p[4])


### the REPL

set_generator_module(all_expr)
check_generator_module()

# loop_parser = yacc(start='expression')

# # testing
# if __name__ == '__main__':
#     env = {}
#     while True:
#         i=input("repl > ")
#         result = loop_parser.parse(input=i, lexer=loop_lexer)
#         print(i,"\n\t",result.eval(env))
