from .while_expr import *

reserved_set |= {
    'IF',
    'THEN',
    'ELSE'
}


# Combine Tokens
tokens = list(token_set | reserved_set)
