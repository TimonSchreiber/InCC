from ply.lex import lex
from ply.yacc import yacc

from language.lexer.proc_expr import *
from language.parser.proc_expr import *
from language.parser.code_generation import set_generator_module, check_generator_module

from compiler.cma import arithmetic_expr
from compiler.cma.x86_64 import to_x86_64, x86_program

set_generator_module(arithmetic_expr)
# check_generator_module(used_procedures_and_classes)

lexer = lex()
parser = yacc(start='expression')
env = {}

ast = parser.parse(input="13-2+47*100")
code_x86 = to_x86_64(ast.code_r(env), env)

print(code_x86)

with open("./cma.s","w") as program_code:
    program_code.write(x86_program(code_x86, env))
