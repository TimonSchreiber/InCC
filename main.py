from ply.lex import lex
from ply.yacc import yacc

from language.lexer.procedure_expr import *
from language.parser.procedure_expr import *
from language.parser.code_generation import set_generator_module, check_generator_module

from interpreter import procedure_expr

set_generator_module(procedure_expr)
check_generator_module(used_procedures_and_classes)

lexer = lex()
parser = yacc(start='expression')
env = procedure_expr.env

counter = r'''
{ counter := acc -> {x -> { acc := acc + x}}
; counter := x -> y -> x := x + y
; c := counter(0)
; a1 := c(1)
; a2 := c(1)
; a3 := c(1)
; a4 := c(2)
; a5 := c(3)
}'''

example = r'''
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
    ; fz := \x-> x*c
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
    { fz := \x,y -> x+y
    ; y := ..x * ..fz(z)
    }
; j := u.fz(3,4)
; k := u..fz(3)
; arr := [.k, 1+f, h]
; lst := list(d, loop e do k := k+1, 3+a, c)
; v := extend struct
    { x := j
    ; y := x * f
    }
    { x := ..x * .y}
; ch := '\n'
; str := "Hello\tworld!"
; l := \x -> ch := x
; m := lock a, ch in
    { a := 3
    ; l(5)
    }
}'''

# currying?
example = r'''
{ f := \x -> x+1
; g := \x,y -> x + y + 2
; h := \x -> \y -> x * y
; a := f(3)
; b := g(4,5)
; c := h(6)
; d := c(7)
}'''


example = r'''
{ g := \x -> struct { h := x }
; a := 3
; s := g(3)
; arr := [s, s.h, s.x]
; t := struct
    { b := 1
    ; c := struct { d := 3 }
    ; e := struct { f := 4 }
    }
; u := struct
    { b := 1
    ; c := g(3)
    ; d := g(4)
    }
; v := struct
    { b := 1
    ; c := struct { d := struct { y := 5} }
    ; d := struct { f := struct { y := 8} }
    ; set := \x -> b := x
    }
; w := struct { set_a := \x -> a := x }
; w.set_a(8)
; z := a
; v.set(3)
}'''

example = r'''
{ x := 2
; f := { local x := 3 in f := \y -> a*x*y }
; a := 5
; x := 7
; b := f(9)
}'''

example = r'''
{
    faktor := 2;
    p := proc (x,y) z,w -> {
        q := proc(x) -> {
            faktor*x
            # faktor := y/z/w sollte fahler produzieren
	    };
        if x=0 then
            z := 1
        else
            z := x+y+p(y,x-1)*q(x);
        w := 2*z;
        w
    };
    p(2,3)
}'''

# example = '''
# { p := proc(a,b) -> a + b
# }'''

example ='''
{
    x := 3;
    f := proc(a) b -> {
        b := x + a;
        g := proc(c) d -> {
            d := c + x
        }
    }
}
'''

result = parser.parse(input=example, lexer=lexer)
r, d = result.eval(env)
print(example, '\n\nresult =>', r, '\n')
for k,v in d.items():
    print(k, ':', v)

# for p in precedence:
#     print(*p)

'''
order:
    00. datatypes
    01. arithmetic_expr
    02. comparison_expr
    04. assignment_expr
    03. boolean_expr
    05. sequence_expr
    06. loop_expr
    07. for_expr
    08. while_expr
    09. ite_expr (If Then Else)
    10. lock_expr
    11. local_expr (acts like letrec)
    12. lambda_expr
    13. struct_expr
    14. procedure_expr

https://en.cppreference.com/w/cpp/language/operator_precedence
'''
