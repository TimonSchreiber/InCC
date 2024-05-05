from .comp_expr import *

token_set |= {'IDENTIFIER', 'ASSIGN'}

t_ASSIGN = r':='

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    val = t.value.upper()
    t.type = val if val in reserved_set else 'IDENTIFIER'
    return t


# Combine Tokens
tokens = list(token_set | reserved_set)

# Create Lexer
assign_lexer = lex()

# Test Lexer
if __name__ == '__main__':
    data = '''
    x := 5.6 < (3 + 6.08)
    y := 2 - 10
    '''

    assign_lexer.input(data)

    for token in assign_lexer:
        print(token)
