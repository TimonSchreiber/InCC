from ply.lex import lex, Lexer
from ply.yacc import yacc, LRParser

from language.lexer.proc_expr import *
from language.parser.proc_expr import *
from language.parser.code_generation import set_generator_module, check_generator_module

from compiler.cma import ite_expr as cmplr
from compiler.cma.x86_64 import to_x86_64, x86_program

set_generator_module(cmplr)
# check_generator_module(used_procedures_and_classes)

lexer: Lexer = lex()
parser: LRParser = yacc(start='expression')
env = {}

program = '''{
    x := 3;
    if x < 2 then
        y := 42
    else
        y := 24
}
'''

ast = parser.parse(input=program, lexer=lexer)
code_x86 = to_x86_64(ast.code_r(env), env)

print(code_x86)

with open("./cma.s","w") as program_code:
    program_code.write(x86_program(code_x86, env))
