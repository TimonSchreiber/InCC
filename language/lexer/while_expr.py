from .for_expr import *

reserved_set |= {
    'WHILE'
}

# Combine Tokens
tokens = list(token_set | reserved_set)


# Test Lexer
if __name__ == '__main__':
    # Create Lexer
    from ply.lex import lex
    while_lexer = lex()
    data = '''
    {
        x := 1;
        y := 2;
        while x < 8 do
        {
            x := x * y;
            y := x - 1
        }
    }
    '''

    while_lexer.input(data)

    for token in while_lexer:
        print(token)
