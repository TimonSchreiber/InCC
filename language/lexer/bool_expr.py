from .assign_expr import *

# Boolean
reserved_set |= {
    'TRUE',
    'FALSE',
    'NOT',
    'AND',
    'NAND',
    'OR',
    'NOR',
    'XOR',
    'EQ',
    'NEQ',
    'IMPL'
}


# Combine Tokens
tokens = list(token_set | reserved_set)

# Create Lexer
bool_lexer = lex()

# Test Lexer
if __name__ == '__main__':
    data = '''
    5.6 < (3 + 6.08) and -8 = 2 - 10
    true xor false
    '''

    bool_lexer.input(data)

    for token in bool_lexer:
        print(token)
