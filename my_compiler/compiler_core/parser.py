import ply.yacc as yacc
from .lexer import tokens

class SyntaxErrorException(Exception):
    pass

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_program(p):
    '''program : instructions'''
    p[0] = p[1]  # AST completo

def p_instructions(p):
    '''instructions : instruction instructions
                   | instruction'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

def p_instruction_write(p):
    '''instruction : WRITE LPAREN write_args RPAREN END'''
    p[0] = ('WRITE', p[3])  # Tupla con tipo de instrucción y argumentos

def p_instruction_write(p):
    '''instruction : WRITE LPAREN write_args RPAREN END'''
    # Modificado para manejar tanto expresiones como strings directos
    p[0] = ('WRITE', p[3])

def p_write_args(p):
    '''write_args : write_args COMMA expression
                 | write_args COMMA STRING
                 | expression
                 | STRING'''
    if len(p) == 2:
        # Manejar tanto strings directos como expresiones
        if isinstance(p[1], str) and p[1][0] == '"' and p[1][-1] == '"':
            p[0] = [('STRING', p[1][1:-1])]  # Quitar las comillas
        else:
            p[0] = [p[1]]
    else:
        if isinstance(p[3], str) and p[3][0] == '"' and p[3][-1] == '"':
            p[0] = p[1] + [('STRING', p[3][1:-1])]
        else:
            p[0] = p[1] + [p[3]]

def p_instruction_capture(p):
    '''instruction : CAPTURE LPAREN ID RPAREN END'''
    p[0] = ('CAPTURE', p[3])  # Tupla con tipo de instrucción y variable

def p_instruction_if(p):
    '''instruction : IF LPAREN condition RPAREN THEN instructions ENDIF'''
    p[0] = ('IF', p[3], p[6])  # Condición y cuerpo del if

def p_instruction_assign(p):
    '''instruction : ID ASSIGN expression END'''
    p[0] = ('ASSIGN', p[1], p[3])  # Asignación: variable y expresión


def p_relop(p):
    '''relop : LT
             | LE
             | GT
             | GE
             | EQ
             | NE'''
    p[0] = p[1]  # Operador como string

def p_expression(p):
    '''expression : expression PLUS term
                 | expression MINUS term'''
    p[0] = ('BINOP', p[2], p[1], p[3])  # Operación binaria estructurada

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]  # Pasa el término directamente

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = ('BINOP', p[2], p[1], p[3])  # Operación binaria estructurada

def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]  # Pasa el factor directamente

def p_factor_num_id(p):
    '''factor : NUMBER
              | ID'''
    p[0] = ('VAR' if isinstance(p[1], str) else 'NUM', p[1])  # Número o variable

def p_factor_expr(p):
    '''factor : LPAREN expression RPAREN'''
    p[0] = p[2]  # Expresión entre paréntesis
    
def p_instruction_while(p):
    '''instruction : WHILE LPAREN condition RPAREN instructions ENDWHILE'''
    p[0] = ('WHILE', p[3], p[5])  # ('WHILE', condición, cuerpo)


        
def p_condition_complex(p):
    '''condition : condition AND condition
                 | condition OR condition
                 | NOT condition
                 | LPAREN condition RPAREN
                 | expression relop expression'''
    if len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]  # Ignorar paréntesis pero mantener estructura
        else:
            p[0] = ('LOGIC', p[2], p[1], p[3])  # Operador lógico
    elif len(p) == 3:
        p[0] = ('NOT', p[2])  # Operador NOT
    else:
        p[0] = ('COMPARISON', p[2], p[1], p[3])  # Comparación simple

def p_error(p):
    if p:
        raise SyntaxErrorException(f"Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        raise SyntaxErrorException("Error de sintaxis al final del archivo.")

parser = yacc.yacc()