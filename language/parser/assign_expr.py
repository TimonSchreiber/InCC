from .comp_expr import *
from ..lexer.assign_expr import tokens#, assign_lexer
import interpreter.all_expr as all_expr

### the generator
# these items are expected to be implemented in module generate (see below)
used_procedures_and_classes |= {
    'VariableExpression',
    'AssignmentExpression'
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
    ['right', 'ASSIGN']
] + precedence


def p_expression_id(p):
    'expression : IDENTIFIER'
    p[0] = gen.VariableExpression(p[1])

def p_expression_assign(p):
    'expression : IDENTIFIER ASSIGN expression'
    p[0] = gen.AssignmentExpression(p[1], p[3])


### the REPL

set_generator_module(all_expr)
check_generator_module()

# assign_parser = yacc(start='expression')

# # testing
# if __name__ == '__main__':
#     env = {}
#     while True:
#         i=input("repl > ")
#         result = assign_parser.parse(input=i, lexer=assign_lexer)
#         print(i,"\n\t",result.eval(env))
