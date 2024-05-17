from .assignment_expr import *

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
