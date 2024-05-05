from language.parser.seque_expr import seque_parser as parser
from language.lexer.seque_expr import seque_lexer as lexer

if __name__ == '__main__':
    env = {}
    while True:
        i=input("repl > ")
        result = parser.parse(input=i, lexer=lexer)
        print(i,"\n\t",result.eval(env))


'''
note:
    1. arith_expr
    2. comp_expr
    3. assign_expr
    4. bool_expr
    5. seque_expr
    6. loop_expr
    7. for_expr
    8. ite_expr (If Then Else)


TODO: https://en.cppreference.com/w/cpp/language/operator_precedence


'''
