from ply.yacc import yacc
from analizadores import lexer

from interprete.instrucciones.instruccion import Instruccion
from interprete.instrucciones.print import Print
from interprete.instrucciones.asignacion import Asignacion
from interprete.instrucciones.declaracion import Declaracion

from interprete.expresiones.expresion import Expresion
from interprete.expresiones.tipoChars import TipoChars
from interprete.expresiones.aritmetica import Aritmetica
from interprete.expresiones.literal import Literal
from interprete.expresiones.acceso import Acceso

from interprete.otros.tipos import *
from interprete.otros.errores import *

tokens = lexer.tokens

# Define la función find_column
def find_column(input_text, token):
    last_cr = input_text.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - last_cr) + 1

def getTextVal(instrucciones):
    text_var = ''
    for instruccion in instrucciones:
        text_var += instruccion.text_val
    return text_var

def tipoToStr(tipo):
    if tipo == TipoDato.INT:
        return 'int'
    elif tipo == TipoDato.FLOAT:
        return 'float'
    elif tipo == TipoDato.STR:
        return 'str'
    #Cambiar por BOOL
    elif tipo == TipoDato.BOOLEAN:
        return 'boolean'
    elif tipo == TipoDato.CHAR:
        return 'char'
    elif isinstance(tipo, TipoChars):
        return tipo.text_val

# precedencia de operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'XOR'),
    ('right', 'NOT'),
    ('left', 'IGUALACION', 'MENOR', 'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL', 'DIFERENCIACION'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('nonassoc', 'POTENCIA', 'MODULO'),
    ('right', 'UMENOS'),
)

# Definición de la gramática

