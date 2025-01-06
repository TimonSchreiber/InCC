import os
import subprocess

from compiler.cma.compiler import code_r as cma_code_r
from compiler.cma.x86_64 import to_x86_64 as cma_to_x86_64

from compiler.mama.compiler import code_b as mama_code_b
from compiler.mama.x86_64 import to_x86_64 as mama_to_x86_64

from compiler.ima24.compiler import code_b as ima24_code_b
from compiler.ima24.x86_64 import to_x86_64 as ima24_to_x86_64

from compiler.util import format_code
from compiler.x86_64 import x86_program

from language.lexer.tokens import lexer
from language.parser.parser import parser

# def ast_to_ic(ast, vm):
#     match vm:
#         case 'cma':
#             env = {}
#             return cma_code_r(ast, env)
#         case 'mama':
#             rho = {}
#             return mama_code_b(ast, rho, 0)

def ast_to_asm(ast: any, vm: str) -> str:
    match vm:
        case 'cma':
            env = {}
            cma_code = cma_to_x86_64(cma_code_r(ast, env))
            program = x86_program(cma_code, env, 'printf')
        case 'mama':
            rho = {}
            mama_code = mama_to_x86_64(mama_code_b(ast, rho, 0))
            program = x86_program(mama_code, rho, 'printf', 'malloc')
        case 'ima24':
            rho = {}
            ima24_code = ima24_to_x86_64(ima24_code_b(ast, rho, 0))
            program = x86_program(ima24_code, rho, 'printf', 'malloc')
    return format_code(program)

def asm_to_obj(asm_file: str, obj_file: str) -> int:
    return subprocess \
        .run(['nasm', '-o', obj_file, '-f', 'elf64', 'asm_file']) \
        .returncode

def obj_to_bin(obj_file: str, bin_file: str) -> int:
    return subprocess \
        .run(['gcc', '-no-pie', '-z', 'noexecstack', '-o', bin_file, obj_file]) \
        .returncode

def main(args):
    match args.file.split('.'):
        case [*_, 'incc24']:
            pass




