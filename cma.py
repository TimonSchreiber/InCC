from ply.lex import lex, Lexer
from ply.yacc import yacc, LRParser

from language.lexer.procedure_expr import *
from language.parser.procedure_expr import *
from language.parser.code_generation import set_generator_module, check_generator_module

from compiler.cma import procedure_expr as cmplr
from compiler.cma.x86_64 import to_x86_64, x86_program, format_code

set_generator_module(cmplr)
# check_generator_module(used_procedures_and_classes)

lexer: Lexer = lex()
parser: LRParser = yacc(start='expression')
env = {}

program = '''
{
    x := 4;
    y := 2;
    while x > 0 do {
        y := y * 2;
        x := x - 1
    };
    y
}
'''

# program = '''
# { p := proc(a,b) x -> a + b
# }'''

ast = parser.parse(input=program, lexer=lexer)
code_x86 = to_x86_64(ast.code_r(env), env)

print(format_code(code_x86))

with open("./cma.s","w") as program_code:
    program_code.write(x86_program(code_x86, env))
