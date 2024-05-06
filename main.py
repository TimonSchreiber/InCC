from language.parser.ite_expr import ite_parser as parser
from language.lexer.ite_expr import ite_lexer as lexer

if __name__ == '__main__':
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
                    b := b+1
        }
        '''
    result = parser.parse(input=i, lexer=lexer)
    print(i,"\n\t",result.eval(env))


'''
note:
    1. arith_expr
    2. comp_expr
    4. assign_expr
    3. bool_expr
    5. seque_expr
    6. loop_expr
    7. for_expr
    8. ite_expr (If Then Else)

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

[o] While expr Do expr

[o] Loacl ident assign expr In expr

class LetExpr()
def init(self, var, value, body):
    ...

def eval(env):
    ?, env = self. -->> Vsiehe skript Seite 50 <<
'''