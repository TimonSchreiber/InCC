from .comparison_expr import *

token_set |= {
    'IDENTIFIER',
    'ASSIGN'
}

t_ASSIGN = r':='

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    val = t.value.upper()
    t.type = val if val in reserved_set else 'IDENTIFIER'
    return t

# Combine Tokens
tokens = list(token_set | reserved_set)
