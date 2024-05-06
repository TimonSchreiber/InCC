from .seque_expr import *

reserved_set |= {
    'LOOP',
    'DO'
}

# Combine Tokens
tokens = list(token_set | reserved_set)


# Test Lexer
if __name__ == '__main__':
    # Create Lexer
    from ply.lex import lex
    loop_lexer = lex()
    data = '''
    loop 5 do
        x := {
            5.6 < (3 + 6.08) and -8 = 2 - 10;
            y := true xor false
        }
    '''
    loop_lexer.input(data)

    for token in loop_lexer:
        print(token)
