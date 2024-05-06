from .bool_expr import *

# Sequences
token_set |= {'BEGIN', 'END', 'SEPARATOR'}

t_BEGIN     = r'{'
t_END       = r'}'
t_SEPARATOR = r';'


# Combine Tokens
tokens = list(token_set | reserved_set)


# Test Lexer
if __name__ == '__main__':
    # Create Lexer
    from ply.lex import lex
    seque_lexer = lex()
    data = '''
    x := {
        5.6 < (3 + 6.08) and -8 = 2 - 10;
        y := true xor false
        }
    '''

    seque_lexer.input(data)

    for token in seque_lexer:
        print(token)
