import ply.lex as lex

# List of token names
tokens = [
    'IDENTIFIER',
    'EQUALS',  'VALOR', 'VARIABLE', 'HASH',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'MENOR', 'MAYOR',
    'SEMICOLON', 'DOTDOT',
    'INT', 'RETURN', 'MAIN', 'INCLUDE', 'IOSTREAM', 'STD', 'COUT'
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
t_HASH = r'\#'
t_DOTDOT = r'\:'
t_MENOR = r'\<'
t_MAYOR = r'\>'

# A regular expression rule with some action code
def t_IDENTIFIER(t):
    r'[a-zA-Z_]\w*'
    if t.value in ['int', 'return', 'main', 'include', 'iostream', 'std', 'cout']:
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
