from loop_expr import *

reserved_set |= {
    'FOR'
}

# Combine Tokens
tokens = list(token_set | reserved_set)

# Create Lexer
for_lexer = lex()

# Test Lexer
if __name__ == '__main__':
    data = '''
    for i:=0; i < x+5; i:= i+2 do
        x := {
            5.6 < (3 + 6.08) and -8 = 2 - 10;
            y := true xor false;
            i * x
        }
    '''

    for_lexer.input(data)

    for token in for_lexer:
        print(token)
