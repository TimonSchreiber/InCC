from ply.lex import lex
from ply.yacc import yacc

from language.lexer.struct_expr import *
from language.parser.struct_expr import *
from language.parser.code_generation import set_generator_module, check_generator_module

from interpreter import struct_expr

set_generator_module(struct_expr)
check_generator_module(used_procedures_and_classes)

lexer = lex()
parser = yacc(start='expression')
env = struct_expr.env

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

example = r'''
{ f := \x -> x+1
; g := \x,y -> x + y + 2
; h := \x -> \y -> x * y
; a := f(3)
; b := g(4,5)
; c := h(6)
; d := c(7)
}'''

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


New feature:
    [x] lock id_list in expr
    [ ] currying
'''
