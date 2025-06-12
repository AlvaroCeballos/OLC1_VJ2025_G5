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
def p_inicio(t):
    '''
    ini : instrucciones
    '''
    t[0] = t[1]
    print('Entrada correcta')

def p_instrucciones(t):
    '''
    instrucciones : instrucciones instruccion
    '''
    t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones_instruccion(t):
    '''
    instrucciones : instruccion
    '''
    t[0] = [t[1]]

def p_instruccion(t):
    '''
    instruccion : instruccion_print PYC
                | declaracion_variable PYC
                | asignacion_variable PYC
    '''
    t[1].text_val += ';\n' 
    t[0] = t[1]

def p_instruccion_print(t):
    '''
    instruccion_print : tipo_print PARA expresion PARC
    '''
    text_val = f'{t[1]}({t[3].text_val})'
    t[0] = Print(text_val=text_val, argumento=t[3], linea=t.lineno(1), columna=t.lexpos(1))

def p_tipo_print(t):
    '''
    tipo_print : PRINT
               | PRINTLN
    '''
    t[0] = t[1]

def p_declaracion_variable(t):
    '''
    declaracion_variable : tipo ID IGUAL expresion
    '''
    text_val = f'{t[2]} {tipoToStr(t[1])}'
    t[0] = Declaracion(text_val, t[2], t[1], t[4].text_val, t.lineno(1), t.lexpos(1))


def p_asignacion_variable(t):
    '''
    asignacion_variable : ID IGUAL expresion
    '''
    text_val = f'{t[1]} = {t[3].text_val}'
    t[0] = Asignacion(text_val, t[1], t[3], t.lineno(1), t.lexpos(1))

# Valores como tal. Eje. 123, "hola", var.
def p_expresion(t):
    '''
    expresion : aritmetica
              | literal
              | relacional
              | logica
    '''
    t[0] = t[1]

def p_expresion_aritmetica(t):
    '''
    aritmetica : expresion SUMA expresion
                | expresion RESTA expresion
                | expresion MULTIPLICACION expresion
                | expresion DIVISION expresion
    '''
    text_val = f'{t[1].text_val} {t[2]} {t[3].text_val}'
    if t[2] == '+':
        t[0] = Aritmetica(text_val=text_val, op1=t[1], operador=TipoAritmetica.SUMA, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))
    elif t[2] == '-':
        t[0] = Aritmetica(text_val=text_val,op1=t[1], operador=TipoAritmetica.RESTA, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))
    elif t[2] == '*':
        t[0] = Aritmetica(text_val=text_val,op1=t[1], operador=TipoAritmetica.MULTIPLICACION, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))
    elif t[2] == '/':
        t[0] = Aritmetica(text_val=text_val,op1=t[1], operador=TipoAritmetica.DIVISION, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))

def p_logica(t):
    '''
    logica : expresion AND expresion
           | expresion OR expresion
           | NOT expresion
    '''
    if len(t) == 4:  # AND or OR
        text_val = f'{t[1].text_val} {t[2]} {t[3].text_val}'
        if t[2] == 'and':
            t[0] = Aritmetica(text_val=text_val, op1=t[1], operador=TipoLogico.AND, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))
        elif t[2] == 'or':
            t[0] = Aritmetica(text_val=text_val, op1=t[1], operador=TipoLogico.OR, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))
    else:  # NOT
        text_val = f'not {t[2].text_val}'
        t[0] = Aritmetica(text_val=text_val, op1=None, operador=TipoLogico.NOT, op2=t[2], linea=t.lineno(1), columna=t.lexpos(1))

def p_relacional(t):
    '''
    relacional : expresion IGUAL expresion
               | expresion DIFERENCIACION expresion
               | expresion MENOR expresion
               | expresion MAYOR expresion
               | expresion MENOR_IGUAL expresion
               | expresion MAYOR_IGUAL expresion
    '''
    text_val = f'{t[1].text_val} {t[2]} {t[3].text_val}'
    if t[2] == '==':
        t[0] = Aritmetica(text_val=text_val, op1=t[1], operador=TipoRelacional.IGUAL, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))
    elif t[2] == '!=':
        t[0] = Aritmetica(text_val=text_val, op1=t[1], operador=TipoRelacional.DESIGUALDAD, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))
    elif t[2] == '<':
        t[0] = Aritmetica(text_val=text_val, op1=t[1], operador=TipoRelacional.MENOR, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))
    elif t[2] == '>':
        t[0] = Aritmetica(text_val=text_val, op1=t[1], operador=TipoRelacional.MAYOR, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))
    elif t[2] == '<=':
        t[0] = Aritmetica(text_val=text_val, op1=t[1], operador=TipoRelacional.MENOR_IGUAL, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))
    elif t[2] == '>=':
        t[0] = Aritmetica(text_val=text_val, op1=t[1], operador=TipoRelacional.MAYOR_IGUAL, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))

def p_entero(t):
    '''
    literal : ENTERO
    '''
    t[0] = Literal(t[1], TipoDato.INT, int(t[1]), t.lineno(1), t.lexpos(1))

def p_cadena(t):
    '''
    literal : CADENAS
    '''
    t[0] = Literal(f"'{t[1]}'", TipoDato.STR, t[1], t.lineno(1), t.lexpos(1))

def p_decimal(t):
    '''
    literal : DECIMAL
    '''
    t[0] = Literal(t[1], TipoDato.FLOAT, float(t[1]), t.lineno(1), t.lexpos(1))

def p_id(t):
    '''
    literal : ID
    '''
    t[0] = Acceso(t[1], t[1], linea=t.lineno(1), columna=t.lexpos(1))

def p_tipo(t):
    '''
    tipo : INT
        | FLOAT
        | STR
        | CHAR
        | BOOLEAN
    '''
    if(t[1] == 'int'):
        t[0] = TipoDato.INT;
    elif(t[1] == 'float'):
        t[0] = TipoDato.FLOAT;
    elif(t[1] == 'char'):
        t[0] = TipoDato.CHAR;
    elif(t[1] == 'boolean'):
        t[0] = TipoDato.BOOLEAN;
    elif(t[1] == 'str'):
        if len(t) == 2:
            t[0] = TipoDato.STR
        else:
            text_val = f'STR({t[3].text_val})'
            t[0] = TipoChars(text_val, TipoDato.STR, t[2]);

# Error sintáctico
def p_error(t):
    if t is not None:
        # Agregando a la tabla de erorres
        err = Error(tipo='Sintáctico', linea=t.lineno, columna=find_column(t.lexer.lexdata, t), descripcion=f'No se esperaba token: {t.value}')
        # Se descarta el token, y el analizador continua
        parser.errok() 
    else:
        # Agregando a la tabla de erorres
        err = Error(tipo='Sintáctico', linea=0, columna=0, descripcion=f'Final inesperado.')
    TablaErrores.addError(err)

# Build the parser
parser = yacc(debug=True)
