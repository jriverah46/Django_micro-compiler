import ply.yacc as yacc
from lexer import tokens

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
    print("Compilación exitosa.")

def p_instructions(p):
    '''instructions : instruction instructions
                    | instruction'''

def p_instruction_write(p):
    '''instruction : WRITE LPAREN write_args RPAREN END'''
    pass

def p_write_args(p):
    '''write_args : expression
                  | STRING
                  | STRING COMMA expression
                  | expression COMMA expression'''

def p_instruction_capture(p):
    '''instruction : CAPTURE LPAREN ID RPAREN END'''
    pass

def p_instruction_if(p):
    '''instruction : IF LPAREN condition RPAREN THEN instructions ENDIF'''
    pass

def p_condition(p):
    '''condition : expression relop expression
                 | condition AND condition
                 | condition OR condition
                 | NOT condition'''

def p_relop(p):
    '''relop : LT
             | LE
             | GT
             | GE
             | EQ
             | NE'''

def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | term'''

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''

def p_factor(p):
    '''factor : NUMBER
              | ID
              | LPAREN expression RPAREN'''
              
def p_instruction_assign(p):
    '''instruction : ID ASSIGN expression END'''
    pass

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' (línea {p.lineno})")
    else:
        print("Error de sintaxis al final del archivo.")

parser = yacc.yacc()
