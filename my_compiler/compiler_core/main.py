# main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from my_compiler.compiler_core.lexer import lexer, lexical_errors, tokenize_code
from my_compiler.compiler_core.parser import parser, SyntaxErrorException

codigo = '''
x = 5 ::

'''

print(parser.parse(codigo, lexer=lexer))
