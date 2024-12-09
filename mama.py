from compiler.mama.compiler import code_b
from compiler.mama.x86_64 import to_x86_64, x86_program

from compiler.util import format_code
from language.lexer.tokens import lexer
from language.parser.parser import parser


program = r'''
    let f := \x -> x in 5
'''

ast = parser.parse(input=program, lexer=lexer)

rho = {}
mama_code_x86 = to_x86_64(code_b(ast, rho, 0))
with open('./mama.s','w') as program_code:
    program_code.write(format_code(x86_program(mama_code_x86, rho)))
