from .struct_expr import *

reserved_set |= {
    'PROC'
}

token_set

# Combine Tokens
tokens = list(token_set | reserved_set)
