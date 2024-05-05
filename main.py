from language.parser.loop_expr import loop_parser as parser
from language.lexer.loop_expr import loop_lexer as lexer

if __name__ == '__main__':
    env = {}
    # while True:
    #     i=input("repl > ")
    i = '''
        {
            x := 1;
            y := 1;
            x := loop x + y * 3 DO
            {
                y := y * 2
            }
        }
        '''
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
