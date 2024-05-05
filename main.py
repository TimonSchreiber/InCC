from language.parser.loop_expr import loop_parser as parser, precedence
from language.lexer.loop_expr import loop_lexer as lexer

if __name__ == '__main__':
    env = {}
    # while True:
    #     i=input("repl > ")
    i = '''
        {
            x := 1;
            y := 1;
            z := loop 6 DO
            {
                y := y * 2
            }
        }
        '''
    result = parser.parse(input=i, lexer=lexer)
    print(i,"\n\t",result.eval(env))
    b = 1
    for lst in precedence:
        print(f'{b} -> {lst}')
        # print(lst)
        b = b+1


'''
note:
    1. arith_expr
    2. comp_expr
    3. bool_expr
    4. assign_expr
    5. seque_expr
    6. loop_expr
    7. for_expr
    8. ite_expr (If Then Else)


https://en.cppreference.com/w/cpp/language/operator_precedence
TODO: precedence of IMPL not mentioned in cpp-reference
'''
