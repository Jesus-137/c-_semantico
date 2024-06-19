import ply.lex as lex

# List of token names
tokens = [
    'IDENTIFIER',
    'EQUALS',  'VALOR', 'VARIABLE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON',
    'INICIO', 'CADENA', 'PROCESO', 'SI', 'VER' , 'FIN', 'ENTERO'
]

# Regular expression rules for simple tokens
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_VARIABLE = r'[a-zA-Z_]\w*'
t_VALOR = r'".*?"|(\d+)'

# A regular expression rule with some action code
def t_IDENTIFIER(t):
    r'[a-zA-Z_]\w*'
    if t.value in ['inicio', 'cadena', 'proceso', 'si', 'ver', 'fin', 'entero']:
        t.type = t.value.upper()
    else:
        t.type = 'VARIABLE'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
