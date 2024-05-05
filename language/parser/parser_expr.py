from ply.yacc import yacc
from ..lexer.arith_expr import tokens, lexer
import expressions

### the generator
# these items are expected to be implemented in module generate (see below)
used_procedures_and_classes = {
    'SelfEvaluatingExpression',
    'BinaryOperatorExpression',
    'UnaryOperatorExpression',
    'ParenthesisExpression',
    'BooleanValueExpression',
    'VariableExpression',
    'AssignmentExpression',
    'SequenceExpression',
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

# TODO: vergleiche cpp references 'precedences'
# https://en.cppreference.com/w/cpp/language/operator_precedence
precedence = [
    ['left', 'ASSIGN'],
    ['left', 'AND', 'OR', 'EQ', 'XOR', 'NAND', 'NOR', 'IMPL'],
    ['left', 'LESS_THEN', 'GREATER_THEN', 'LESS_EQUALS', 'GREATER_EQUALS', 'EQUALS', 'NOT_EQUALS'],
    ['left', 'PLUS', 'MINUS'],
    ['left', 'TIMES', 'DIVIDE'],
    ['right', 'UMINUS', 'NOT'],
]

def p_expression_number(p):
    '''expression : NUMBER
                  | FLOAT'''
    p[0] = gen.SelfEvaluatingExpression(p[1])

def p_expression_unary(p):
    '''expression : MINUS expression %prec UMINUS
                  | NOT expression'''
    p[0] = gen.UnaryOperatorExpression(p[1], p[2])

def p_expression_binary(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression LESS_THEN expression
                  | expression GREATER_THEN expression
                  | expression LESS_EQUALS expression
                  | expression GREATER_EQUALS expression
                  | expression EQUALS expression
                  | expression NOT_EQUALS expression
                  | expression AND expression
                  | expression OR expression
                  | expression EQ expression
                  | expression XOR expression
                  | expression NAND expression
                  | expression NOR expression
                  | expression IMPL expression'''
    p[0] = gen.BinaryOperatorExpression(p[1], p[2], p[3])

def p_expression_boolean_value(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = gen.BooleanValueExpression(p[1])

def p_expression_parenthesis(p):
    'expression : LPAREN expression RPAREN'
    p[0] = gen.ParenthesisExpression(p[2])

def p_expression_id(p):
    'expression : IDENTIFIER'
    p[0] = gen.VariableExpression(p[1])

def p_expression_assign(p):
    'expression : IDENTIFIER ASSIGN expression'
    p[0] = gen.AssignmentExpression(p[1], p[3])

def p_expression_sequence(p):
    'expression : BEGIN body END'
    p[0] = gen.SequenceExpression(p[2])

def p_bodyn(p):
    '''body : expression
            | body SEPARATOR expression'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]


def p_error(p):
    print("Syntax error in input!")


### the REPL

set_generator_module(expressions)
check_generator_module()

parser = yacc(start='expression')

# testing
if __name__ == '__main__':
    env = {}
    while True:
        i=input("repl > ")
        result = parser.parse(input=i, lexer=lexer)
        print(i,"\n\t",result.eval(env))
