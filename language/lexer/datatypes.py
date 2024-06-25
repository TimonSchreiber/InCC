reserved_set = {
    'LIST',
    'ARRAY'
}

token_set = {
    'FLOAT',
    'NUMBER',
    'CHAR',
    'STRING',
    'LBRACKET',
    'RBRACKET'
}

t_LBRACKET = r'\['
t_RBRACKET = r'\]'

def t_FLOAT(t):
    r'\d*\.\d+|\d+\.'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHAR(t):
    r'\'(\\t|\\n|\\\'|\\\"|\\\\|[^\\])\''
    t.value = t.value[1:-1]
    return t

def t_STRING(t):
    r'\"(\\t|\\n|\\\'|\\\"|\\\\|[^\\])*?\"'
    t.value = t.value[1:-1]
    return t

# Ignore, Comments, and Error handling
t_ignore  = ' \t\n'

t_ignore_COMMENT = r'\#.*'

def t_error(t):
    print(f'Illegal character {t.value[0]}')
    t.lexer.skip(1)

# Combine Tokens
tokens = list(token_set | reserved_set)
