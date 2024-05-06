from .arith_expr import *

# Comparison
token_set |= {
    'LESS_THEN',
    'GREATER_THEN',
    'LESS_EQUALS',
    'GREATER_EQUALS',
    'EQUALS',
    'NOT_EQUALS'
}

t_LESS_THEN         = r'<'
t_GREATER_THEN      = r'>'
t_LESS_EQUALS       = r'<='
t_GREATER_EQUALS    = r'>='
t_EQUALS            = r'='
t_NOT_EQUALS        = r'!='

# Combine Tokens
tokens = list(token_set | reserved_set)


# Test Lexer
if __name__ == '__main__':
    # Create Lexer
    from ply.lex import lex
    comp_lexer = lex()
    data = '''
    5.6 < (3 + 6.08)
    -8 = 2 - 10
    '''

    comp_lexer.input(data)

    for token in comp_lexer:
        print(token)
