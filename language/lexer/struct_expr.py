from .lambda_expr import *

reserved_set |= {
    'STRUCT',
    'EXTEND'
}

token_set |= {
    'DOT'
}

t_DOT = r'\.'

# Combine Tokens
tokens = list(token_set | reserved_set)
