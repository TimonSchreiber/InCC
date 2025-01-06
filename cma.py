from compiler.cma.compiler import code_r
from compiler.cma.x86_64 import to_x86_64

from compiler.util import format_code
from compiler.x86_64 import x86_program
from language.lexer.tokens import lexer
from language.parser.parser import parser

## TODO: deprecated --> delete and use a real compiler to compile and run *.incc24 files

program = '''
{
    x := 3;
    f := proc(a) b -> {
        b := x + a;
        g := proc(c,e) d -> {
            d := -c * x - e
            # d := b + x # Nicht erlaubt!
        };
        g(b,7)
    };
    f(3) / 5;
    5 > 1
}
'''

program = '''{
    a := 4;
    f := proc(b) c ->  c := a+b;
    f(3)
}
'''


ast = parser.parse(input=program, lexer=lexer)

env = {}
cma_code_x86 = to_x86_64(code_r(ast, env))
with open('./cma.s','w') as program_code:
    program_code.write(format_code(x86_program(cma_code_x86, env, 'printf')))
