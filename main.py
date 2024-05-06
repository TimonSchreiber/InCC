from ply.lex import lex
from ply.yacc import yacc
from language.lexer.ite_expr import *
from language.parser.ite_expr import *

lexer = lex()
parser = yacc(start='expression')
env = {}
# while True:
#     i=input("repl > ")
i = '''
    {
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
    }
    '''

result = parser.parse(input=i, lexer=lexer)
print(i,"\n\t",result.eval(env))


'''
note:
    01. arith_expr
    02. comp_expr
    04. assign_expr
    03. bool_expr
    05. seque_expr
    06. loop_expr
    07. for_expr
    09. while_expr
    08. ite_expr (If Then Else)
    10. lock_expr ~
    11. local_expr ~

https://en.cppreference.com/w/cpp/language/operator_precedence
TODO: precedence of IMPL not mentioned in cpp-reference
'''

'''
[x] loop expr do expr
[x] for assign; bool_expr; assign do expr
[O] [for assign; bool_expr; assign do lock var expr]  <--  optional
        -> Lock ident In expr

[x] if expr then expr
[x] if expr then expr else expr

[x] While expr Do expr

[o] Local ident assign expr In expr

class LetExpr()
def init(self, var, value, body):
    ...

def eval(env):
    ?, env = self. -->> Vsiehe skript Seite 50 <<

'''