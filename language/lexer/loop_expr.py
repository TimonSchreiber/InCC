from .sequence_expr import *

reserved_set |= {
    'LOOP',
    'DO'
}

# Combine Tokens
tokens = list(token_set | reserved_set)
