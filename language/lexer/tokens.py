from ply.lex import lex

reserved_set = {
    'LIST',
    'ARRAY',
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
    'IMPL',
    'LOOP',
    'DO',
    'FOR',
    'WHILE',
    'IF',
    'THEN',
    'ELSE',
    'LOCK',
    'IN',
    'LET',
    'LETREC',
    'STRUCT',
    'EXTEND',
    'PROC',
}

token_set = {
    'FLOAT',
    'NUMBER',
    'CHAR',
    'STRING',
    'LBRACKET',
    'RBRACKET',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LESS_THEN',
    'GREATER_THEN',
    'LESS_EQUALS',
    'GREATER_EQUALS',
    'EQUALS',
    'NOT_EQUALS',
    'LPAREN',
    'RPAREN',
    'IDENTIFIER',
    'ASSIGN',
    'BEGIN',
    'END',
    'SEPARATOR',
    'ARROW',
    'COMMA',
    'LAMBDA',
    'DOT',
}

t_LBRACKET       = r'\['
t_RBRACKET       = r'\]'
t_PLUS           = r'\+'
t_MINUS          = r'-'
t_TIMES          = r'\*'
t_DIVIDE         = r'/'
t_LESS_THEN      = r'<'
t_GREATER_THEN   = r'>'
t_LESS_EQUALS    = r'<='
t_GREATER_EQUALS = r'>='
t_EQUALS         = r'='
t_NOT_EQUALS     = r'!='
t_LPAREN         = r'\('
t_RPAREN         = r'\)'
t_ASSIGN         = r':='
t_BEGIN          = r'{'
t_END            = r'}'
t_SEPARATOR      = r';'
t_ARROW          = r'->'
t_COMMA          = r','
t_LAMBDA         = r'\\'
t_DOT            = r'\.'

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

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    val = t.value.upper()
    t.type = val if val in reserved_set else 'IDENTIFIER'
    return t

# Ignore, Comments, and Error handling
t_ignore  = ' \t\n'

t_ignore_COMMENT = r'\#.*'

def t_error(t):
    print(f'Illegal character {t.value[0]}')
    t.lexer.skip(1)

# Combine Tokens
tokens = list(token_set | reserved_set)

lexer = lex()
