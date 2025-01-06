# incc/incc.py

'https://docs.python.org/3/howto/argparse.html'

import argparse

from compiler.cma.compiler import code_r
from compiler.cma.x86_64 import to_x86_64 as cma_to_x86_64

from compiler.mama.compiler import code_b
from compiler.mama.x86_64 import to_x86_64 as mama_to_x86_64

from compiler.compiler import x86_program
from interpreter.interpreter import eval

from language.lexer.tokens import lexer
from language.parser.parser import parser

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(prog='InCC24', description="Execute or compile an incc program.")
    arg_parser.add_argument("mode", choices=["interpret", "compile"], help="Choose to interpret or compile the incc program.")
    arg_parser.add_argument("source_file", type=str, help="The .incc source file to interpret or compile.")

    args = arg_parser.parse_args()

    # Read the source file
    with open(args.source_file, 'r') as file:
        source_code = file.read()

    # Run either the interpreter or compiler based on the mode
    env = {}
    ast = parser.parse(input=source_code, lexer=lexer)
    if args.mode == "interpret":
        r = eval(ast, env)

        print('\nresult =>', r, '\n')

        for k,v in env.items():
            print(k, ':', v)
    elif args.mode == "compile":
        code_x86 = cma_to_x86_64(code_r(ast, env), env)

        asm_code = code_r(source_code, env)

        with open('./cma.s','w') as program_code:
            program_code.write(x86_program(code_x86, env, 'printf'))
