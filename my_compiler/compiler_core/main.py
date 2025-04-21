# main.py
from .lexer import lexer
from .parser import parser

codigo = '''
if(x>y) then 
    x=x+1:: 
end-if
'''

print(parser.parse(codigo, lexer=lexer))
