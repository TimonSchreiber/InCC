# from ply.lex import lex

# Initial reserved key words
reserved_set = set()

# Arithmetics
token_set = {
   'FLOAT',
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
}

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Ignore and Error handling
t_ignore  = ' \t\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Combine Tokens
tokens = list(token_set | reserved_set)

# Create Lexer


# Test Lexer
if __name__ == '__main__':
    from ply.lex import lex
    arith_lexer = lex()
    data = '''
    5.6 * (3 + 6.08)
    -8 / 2 - 10
    '''

    arith_lexer.input(data)

    for token in arith_lexer:
        print(token)
