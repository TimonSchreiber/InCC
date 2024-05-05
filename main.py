from language.parser.for_expr import for_parser as parser, precedence
from language.lexer.for_expr import for_lexer as lexer

if __name__ == '__main__':
    env = {}
    # while True:
    #     i=input("repl > ")
    i = '''
        {
            y := 0;
            z := for x := 0; x > 3; x := x + 1 DO
            {
                y := y + 2
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
Loop / For
---
loop expr do expr
for assign; bool_expr; assign do expr
[for assign; bool_expr; assign do lock var expr]  <--  optional
'''
# Was ist der Rückgabewert der Loop-Expression?
# Das Ergebnis der letzen Expression im Körper?
#   -> Was, wenn der Körper gar nicht ausgeführt wurde? 'None'?!


'''
If Then Else
---

IF bool_expr THEN expr
IF bool_expr THEN expr ELSE expr
'''

# precedence 'ELSE' > 'THEN'