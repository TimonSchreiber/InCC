from .assign_expr import *

# Boolean
reserved_set |= {
    'TRUE',
    'FALSE',
    'NOT',
    'AND',
    'OR',
    'EQ',
    'XOR',
    'NAND',
    'NOR',
    'IMPL'
}

t_NOT   = r'not'
t_AND   = r'and'
t_OR    = r'or'
t_EQ    = r'eq'
t_XOR   = r'xor|neq'
t_NAND  = r'nand'
t_NOR   = r'nor'
t_IMPL  = r'impl'


# Combine Tokens
tokens = list(token_set | reserved_set)

# Create Lexer
bool_lexer = lex()

# Test Lexer
if __name__ == '__main__':
    data = '''
    x := 5.6 < (3 + 6.08) and -8 = 2 - 10
    y := true xor false
    '''

    bool_lexer.input(data)

    for token in bool_lexer:
        print(token)
