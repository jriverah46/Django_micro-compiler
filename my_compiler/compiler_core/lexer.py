import ply.lex as lex
lexical_errors=[]
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


# Ignorar espacios, tabulaciones y saltos de línea
t_ignore = ' \t\r'
def t_newline(t):
    r'\r?\n+'
    t.lexer.lineno += t.value.count("\n")  

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



def t_error(t):
    error_msg = f"Caracter ilegal '{t.value[0]}' en la línea {t.lineno}"
    lexical_errors.append(error_msg)
    t.lexer.skip(1)

lexer = lex.lex()

def tokenize_code(code):
    lexer.input(code)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(tok)
    return tokens_list
