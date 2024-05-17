from ply.lex import lex
from ply.yacc import yacc

from language.lexer.local_expr import *
from language.parser.local_expr import *
from language.parser.code_generation import set_generator_module, check_generator_module

from interpreter import local_expr as interp
from interpreter.enviroment import Enviroment

set_generator_module(interp)
check_generator_module(used_procedures_and_classes)

lexer = lex()
parser = yacc(start='expression')
env = Enviroment({})

i = '''
{
    a := 3;
    b := 4;
    c := True;
    x := 4;
    y := 4;


    # z :=
    # if x > y then
    #     if x > y then
    #         y := y + 1
    #     else
    #         x*y;
    # z := 2;
    # a := 0;
    # b := 0;
    # loop x do
    #     if z >= 0 then
    #         loop y do
    #             {
    #                 z := z - 1;
    #                 a := a + 1
    #             }
    #     else
    #         b := b+1;
    # while x > z do
    #     x := x - 1

    # local a := 4 in
    # {
    #     b := a + 2;
    #     a := a * a;
    #     c := a + 2
    # }

    # lock a in
    # {
    #     a := 4;
    #     b := a * b;
    #     c := True
    # }

    while a > 0 do
    {
        a := a - 1;
        b := b * 2;
        c := c xor True;
        d := 6
    }
}
'''

result = parser.parse(input=i, lexer=lexer)
print(i,"\n",result.eval(env))


'''
note:
    01. arithmetic_expr
    02. comparison_expr
    04. assignment_expr
    03. boolean_expr
    05. sequence_expr
    06. loop_expr
    07. for_expr
    08. while_expr
    09. ite_expr (If Then Else)
    10. TODO: lock_expr
    11. TODO: local_expr

https://en.cppreference.com/w/cpp/language/operator_precedence
'''
