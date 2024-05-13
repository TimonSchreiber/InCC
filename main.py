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

a = '''{
    x := 4;
    y := 4;
    z:=if x > y then
        if x > y then
            y := y + 1
    else
        x*y;
    z := 2;
    a := 0;
    b := 0;
    loop x do
        if z >= 0 then
            loop y do
                {
                    z := z - 1;
                    a := a + 1
                }
        else
            b := b+1;
    while x > z do
        x := x - 1
}'''

b = '''{
    a := 3;
    lock a in
    {
        b := a + 2;
        a := a * a;
        c := a + 2
    }
}'''

result = parser.parse(input=b, lexer=lexer)
print(a,"\n",result.eval(env))


'''
note:
    01. arith_expr
    02. comp_expr
    04. assign_expr
    03. bool_expr
    05. seque_expr
    06. loop_expr
    07. for_expr
    08. while_expr
    09. ite_expr (If Then Else)
    10. TODO: lock_expr
    11. TODO: local_expr

https://en.cppreference.com/w/cpp/language/operator_precedence
'''
