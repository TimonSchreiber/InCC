from ply.lex import lex
from ply.yacc import yacc

from language.lexer.struct_expr import *
from language.parser.struct_expr import *
from language.parser.code_generation import set_generator_module, check_generator_module

from interpreter import struct_expr
# from interpreter.enviroment import Enviroment

set_generator_module(struct_expr)
check_generator_module(used_procedures_and_classes)

lexer = lex()
parser = yacc(start='expression')
env = struct_expr.env

example = '''
{ x := True
; local x := False in
    b := 1
; lock x in
    { a := 3
    ; b := 4
    ; c := True
    ; y := 4
    }
; z :=
    if x > y then
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
        x := x - 1;

    local a := 4 in
        local b := 7 in
        {
            d := a + b;
            a := a * a;
            c := a + 2;
            e := True
        };

    for i := 0; i < 5; i := i+1 do
        lock a in
        {
            a := 4;
            b := a * b;
            c := True
        };

    while a > 0 do
    {
        a := a - 1;
        b := b * 2;
        c := c xor True;
        d := 6
    };

    a := x -> x+1;
    b := a(2);
    c := b + a(7)

    a := 4;
    f := x -> y -> a := a+y;
    b := f(2)(3)
}
'''

# local as letrec
example = '''
{
    g := local gauss := x ->
        if x = 0 then 0
        else x + gauss(x - 1) in
            gauss(10);
    f := local fac := x ->
        if x = 0 then 1
        else x * fac(x - 1) in
            fac(8);
    a := 'a';
    s := "ghj";
    n := ""
}
'''

example = '''
{ arr := [1,2,4,8]
; b := arr[0]
; c := arr[3]
; d := arr[b+1]
; lst := list(1,2,4,8)
; e := head(lst)
; f := tail(lst)
; h := cons('A', f)
; i := [[1,2],3,4]
; j := i[0]
; k := j[0]
; l := [3+b]
# ; m := [3+b, b]
}'''

# example = '''
# { a := 'a'
# ; b := "a"
# ; c := '\n'
# ; d := "hello\tworld\n!"
# }
# '''

# example = '''
# { a := 'a'
# # ; b := '\n'
# # ; c := '\t'
# # ; d := '\\'
# # ; e := b = '\t
# '''

# example = '''
# { a := 5
# ; f := x -> x+1
# ; b := f(a)
# }'''

# '''
# ; f := "test"
# ; g := "a\nb"
# ; h := "Hello \"world\"!"
# }'''

# '''
# # ; h := "Hello "world"!"
# # ; i := "\t\n\r\'\"\\"'''

# struct
example = '''
{ a := 5
; local a := 6 in
    b := 2 * a
; c := for i := a; i >= 0; i := i-1 do
    a := a+1
; lock c in
    a := a - c / 2
; s := struct
    { x := c+2
    ; y := 3
    ; fz := x-> x*c
    ; a := True
    }
; d := s.x
; e := s.fz(2)
; t := extend s
    { x := 47
    ; z := 11
    }
; f := t.z
; g := t.x
; h := t..x
; u := extend t
    { fz := x,y -> x+y
    ; y := a        # TODO: how to access x from s and not x from t
    }
; j := u.fz(3,4)
; k := u..fz(3)
}'''

result = parser.parse(input=example, lexer=lexer)
# # example = '\n'.join(repr(example).strip('\"').split(';'))
print(example, '\n', result.eval(env))

# for p in precedence:
#     print(*p)

'''
order:
    00. datatypes
    01. arithmetic_expr
    02. comparison_expr
    04. assignment_expr
    03. boolean_expr
    05. sequences_expr
    06. loop_expr
    07. for_expr
    08. while_expr
    09. ite_expr (If Then Else)
    10. lock_expr
    11. local_expr (acts like letrec)
    12. lambda_expr
    13. struct_expr

https://en.cppreference.com/w/cpp/language/operator_precedence
'''
