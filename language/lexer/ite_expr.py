from .while_expr import *

reserved_set |= {
    'IF',
    'THEN',
    'ELSE'
}

# Combine Tokens
tokens = list(token_set | reserved_set)

# Create Lexer
ite_lexer = lex()

# Test Lexer
if __name__ == '__main__':
    data = '''
    if x > 9 THEN
    for i:=0; i < x+5; i:= i+2 do
        x := {
            5.6 < (3 + 6.08) and -8 = 2 - 10;
            y := true xor false;
            i * x
        }
    else
        x := true
    '''

    ite_lexer.input(data)

    for token in ite_lexer:
        print(token)
