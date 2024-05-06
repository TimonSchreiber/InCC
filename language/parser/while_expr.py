from .for_expr import *
from ..lexer.while_expr import tokens#, while_lexer
import interpreter.all_expr as all_expr

### the generator
# these items are expected to be implemented in module generate (see below)
used_procedures_and_classes |= {
    'WhileExpression'
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

def p_expression_while(p):
    'expression : WHILE expression DO expression'
    p[0] = gen.WhileExpression(p[2], p[4])


### the REPL

set_generator_module(all_expr)
check_generator_module()

# while_parser = yacc(start='expression')

# # testing
# if __name__ == '__main__':
#     env = {}
#     while True:
#         i=input("repl > ")
#         result = while_parser.parse(input=i, lexer=while_lexer)
#         print(i,"\n\t",result.eval(env))
