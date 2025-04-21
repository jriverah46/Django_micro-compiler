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
    p[0] = "Compilación exitosa."

def p_instructions(p):
    '''instructions : instruction instructions
                    | instruction'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

def p_instruction_write(p):
    '''instruction : WRITE LPAREN write_args RPAREN END'''
    p[0] = f"Escribir: {p[3]}"

def p_write_args(p):
    '''write_args : expression
                  | STRING
                  | STRING COMMA expression
                  | expression COMMA expression'''
    p[0] = p[1:]

def p_instruction_capture(p):
    '''instruction : CAPTURE LPAREN ID RPAREN END'''
    p[0] = f"Captura de ID: {p[3]}"

def p_instruction_if(p):
    '''instruction : IF LPAREN condition RPAREN THEN instructions ENDIF'''
    p[0] = f"Condición: {p[3]} ejecutada con instrucciones {p[6]}"

def p_instruction_assign(p):
    '''instruction : ID ASSIGN expression END'''
    p[0] = f"Asigna {p[3]} a {p[1]}"

def p_condition(p):
    '''condition : expression relop expression
                 | condition AND condition
                 | condition OR condition
                 | NOT condition'''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    else:
        p[0] = (p[1], p[2])

def p_relop(p):
    '''relop : LT
             | LE
             | GT
             | GE
             | EQ
             | NE'''
    p[0] = p[1]

def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    p[0] = (p[1], p[2], p[3])

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = (p[1], p[2], p[3])

def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]

def p_factor_num_id(p):
    '''factor : NUMBER
              | ID'''
    p[0] = p[1]

def p_factor_expr(p):
    '''factor : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_error(p):
    if p:
        raise SyntaxErrorException(f"Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        raise SyntaxErrorException("Error de sintaxis al final del archivo.")

parser = yacc.yacc()
