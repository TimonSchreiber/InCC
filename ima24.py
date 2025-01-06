## TODO: deprecated --> delete and use a real compiler to compile and run *.incc24 files

from compiler.ima24.compiler import code_b
from compiler.ima24.x86_64 import to_x86_64

from compiler.util import format_code
from compiler.x86_64 import x86_program
from language.lexer.tokens import lexer
from language.parser.parser import parser

program = r'''
    x := 21
'''

ast = parser.parse(input=program, lexer=lexer)

rho = {}
mama_code_x86 = to_x86_64(code_b(ast, rho, 0))
with open('./ima24.s','w') as program_code:
    program_code.write(format_code(x86_program(mama_code_x86, rho, 'printf', 'malloc')))
