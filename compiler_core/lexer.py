import ply.lex as lex

# Palabras clave
reserved = {
    'write': 'WRITE',
    'capture': 'CAPTURE',
    'if': 'IF',
    'then': 'THEN',
    'end-if': 'ENDIF',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT'
}

# Lista de tokens
tokens = [
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',
    'ASSIGN', 'LPAREN', 'RPAREN', 'COMMA', 'END'
] + list(reserved.values())

# Reglas de expresiones regulares
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQ      = r'=='
t_NE      = r'<>'
t_LE      = r'<='
t_LT      = r'<'
t_GE      = r'>='
t_GT      = r'>'
t_ASSIGN  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA   = r','
t_END     = r'::'

t_ignore = ' \t'

def t_STRING(t):
    r'\".*?\"'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_-]*'
    if t.value == 'end-if':
        t.type = 'ENDIF'
    else:
        t.type = reserved.get(t.value, 'ID')  # Puede ser palabra reservada o ID
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
