from ply.yacc import yacc
from analizadores import lexer

from interprete.instrucciones.instruccion import Instruccion
from interprete.instrucciones.print import Print
from interprete.instrucciones.asignacion import Asignacion
from interprete.instrucciones.declaracion import Declaracion
from interprete.instrucciones.iWhile import While
from interprete.instrucciones.iCase import Case
from interprete.instrucciones.iSwitch import Switch
from interprete.instrucciones.iBrake import Break
from interprete.instrucciones.iFor import For 
from interprete.instrucciones.instruccion_if import Instruccion_if
from interprete.instrucciones.iDoWhile import DoWhile
from interprete.instrucciones.pcontinue import Continue
from interprete.otros.enviroment import Enviroment

from interprete.expresiones.expresion import Expresion
from interprete.expresiones.tipoChars import TipoChars
from interprete.expresiones.aritmetica import Aritmetica
from interprete.expresiones.relacional import Relacional
from interprete.expresiones.logica import Logica
from interprete.expresiones.literal import Literal
from interprete.expresiones.acceso import Acceso
from interprete.expresiones.nativas import Seno, Coseno, Inv
from interprete.instrucciones.vector import Vector

from interprete.otros.tipos import *
from interprete.otros.errores import *
from interprete.otros.errores import Error, TablaErrores

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
    elif tipo == TipoDato.BOOL:
        return 'bool'
    elif tipo == TipoDato.CHAR:
        return 'char'
    elif isinstance(tipo, TipoChars):
        return tipo.text_val

# precedencia de operadores
precedence = (
    ('right', 'UMENOS'),
    
    ('left', 'AND'), 
    ('left', 'OR'),
    ('left', 'XOR'),
    ('right', 'NOT'),
    ('left', 'IGUALACION', 'MENOR', 'MAYOR', 'MENOR_IGUAL', 'MAYOR_IGUAL', 'DIFERENCIACION'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('nonassoc', 'POTENCIA', 'MODULO'),
    
)

# Definición de la gramática
def p_inicio(t):
    '''
    ini : instrucciones
    '''
    t[0] = t[1] if t[1] is not None else []
    print('Entrada correcta')

def p_instrucciones(t):
    '''
    instrucciones : instrucciones instruccion
    '''
    #if t[1] is None:
     #   t[1] = []
    #if t[2] is None:
     #   t[2] = []
    #t[1].append(t[2])
    #t[0] = t[1]
    t[0] = t[1] + [t[2]]


def p_instruccion_error_print(t):
    '''
    instruccion : error PYC
    '''
    # Error en instrucción con punto y coma - ya manejado por p_error
    t[0] = None

def p_instruccion_error_estructura(t):
    '''
    estructura_control : error
    '''
    # Error en estructura de control - ya manejado por p_error
    t[0] = None

def p_instrucciones_error(t):
    '''
    instrucciones : instrucciones error
                  | error
    '''
    # Si hay error en una instrucción, continuar con las demás
    if len(t) == 3:  # instrucciones error
        t[0] = t[1] if t[1] is not None else []
    else:  # solo error
        t[0] = []

def p_expresion_error(t):
    '''
    expresion : error
    '''
    # Error en expresión - retornar expresión nula
    t[0] = Literal('ERROR', TipoDato.ERROR, None, 0, 0)

def p_instrucciones_empty(t):
    'instrucciones : '
    t[0] = []

def p_instrucciones_instruccion(t):
    '''
    instrucciones : instruccion
    '''
    if t[1] is None:
        t[0] = []
    else:
        t[0] = [t[1]]

def p_instruccion(t):
    '''
    instruccion : instruccion_println
                | declaracion_variable PYC
                | asignacion_variable PYC
                | estructura_control
                | incremento PYC
                | decremento PYC
                | declaracion_vector PYC 
    '''
    if len(t) == 3:  # Instrucciones que terminan con PYC
        if t[1] is not None and hasattr(t[1], 'text_val'):
            t[1].text_val += ';\n'
            t[0] = t[1]
        else:
            t[0] = None  # Instrucción inválida, ignórala
    else:  # while, for, if, etc.
        t[0] = t[1]

def p_declaracion_vector(t):
    '''
    declaracion_vector : VECTOR CORCHETE_ABRE tipo CORCHETE_CIERRA ID PARA lista_dimensiones PARC
                       | VECTOR CORCHETE_ABRE tipo CORCHETE_CIERRA ID PARA lista_dimensiones PARC IGUAL lista_valores_iniciales
    '''
    if len(t) == 9:  # Sin valores iniciales
        text_val = f'Vector[{t[3].name.lower()}] {t[5]}({", ".join([str(d.valor) for d in t[7]])})'
        t[0] = Vector(
            text_val=text_val,
            id=t[5],
            tipo_dato=t[3],
            dimensiones=t[7],
            valores_iniciales=None,
            linea=t.lineno(1),
            columna=t.lexpos(1)
        )
    else:  # Con valores iniciales (len(t) == 11)
        text_val = f'Vector[{t[3].name.lower()}] {t[5]}({", ".join([str(d.valor) for d in t[7]])}) = ...'
        t[0] = Vector(
            text_val=text_val,
            id=t[5],
            tipo_dato=t[3],
            dimensiones=t[7],
            valores_iniciales=t[10],
            linea=t.lineno(1),
            columna=t.lexpos(1)
        )

def p_lista_dimensiones(t):
    '''
    lista_dimensiones : lista_dimensiones COMA expresion
                     | expresion
    '''
    if len(t) == 4:  # lista_dimensiones COMA expresion
        t[0] = t[1] + [t[3]]
    else:  # expresion
        t[0] = [t[1]]

def p_lista_valores_iniciales(t):
    '''
    lista_valores_iniciales : lista_valores_iniciales COMA CORCHETE_ABRE lista_expresiones CORCHETE_CIERRA
                           | CORCHETE_ABRE lista_expresiones CORCHETE_CIERRA
    '''
    if len(t) == 6:  # lista_valores_iniciales COMA [expresiones]
        t[0] = t[1] + [t[4]]
    else:  # [expresiones]
        t[0] = [t[2]]

def p_lista_expresiones(t):
    '''
    lista_expresiones : lista_expresiones COMA expresion
                     | expresion
    '''
    if len(t) == 4:  # lista_expresiones COMA expresion
        t[0] = t[1] + [t[3]]
    else:  # expresion
        t[0] = [t[1]]

#Se crea funcion para poder manejar todos los tipos de ciclos anidados
def p_estructura_control(t):
    '''
    estructura_control : instruccion_while
                       | instruccion_if
                       | instruccion_switch
                       | instruccion_dowhile
                       | instruccion_for
    '''
    # estrcutura control | instruccion_if | instruccion_for | instruccion_switch
    t[0] = t[1]

def p_instruccion_while(t):
    '''
    instruccion_while : WHILE PARA expresion PARC LLA instrucciones LLC
    '''
    text_val = f'while({t[3].text_val}) ' + '{\n'
    for inst in t[6]:
        text_val += f'    {inst.text_val}'
    text_val += '}\n'
    
    t[0] = While(text_val=text_val, condicion=t[3], instrucciones=t[6], 
                 linea=t.lineno(1), columna=t.lexpos(1))
#expresion para estructura for
def p_instruccion_for(t):
    '''
    instruccion_for : FOR PARA declaracion_variable PYC expresion PYC actualizacion PARC LLA instrucciones LLC
    
    '''
    text_val = f'for ({t[3].text_val}; {t[5].text_val}; {t[7].text_val}) ' + '{\n'
    for inst in t[10]:
        text_val += f'    {inst.text_val}'
    text_val += '}\n'

    t[0] = For(
        text_val= text_val,
        inicializacion = t[3],
        condicion = t[5],
        incremento = t[7],
        instrucciones = t[10],
        linea = t.lineno(1),
        columna = t.lexpos(1)
    )

#expresion para actualizacion
def p_actualizacion(t):
    '''actualizacion : incremento
                   | decremento
                   | expresion
                   | asignacion_variable
    '''
    t[0] = t[1]
#expresin para definir estructura switch
def p_instruccion_switch(t):
    '''
    instruccion_switch : SWITCH PARA expresion PARC LLA lista_case default_opcional LLC
    '''
    t[0] = Switch(
        text_val = '...',
        condicion = t[3],
        casos = t[6],
        default = t[7],
        linea = t.lineno(1),
        columna = t.lexpos(1)
    )

#expresion para definir estructura do while
def p_instruccion_dowhile(t):
    '''
    instruccion_dowhile : DO LLA instrucciones LLC WHILE PARA expresion PARC PYC
    '''
    text_val = 'do {\n'
    for inst in t[3]:
        text_val += f'    {inst.text_val}'
    text_val += '} while(' + f'{t[7].text_val}' + ');\n'
    
    t[0] = DoWhile(text_val=text_val, instrucciones=t[3], condicion=t[7], 
                   linea=t.lineno(1), columna=t.lexpos(1))

#expresion que define la lista de los cases

def p_lista_case(t):
    '''
    lista_case : lista_case case_unico
                | case_unico

    '''
    if len(t) == 3:
        t[0] = t[1] +[t[2]]
    else:
        t[0] = [t[1]]
#definimos la estructura de un case
def p_case_unico(t):
    '''
    case_unico : CASE expresion DOS_PUNTOS instrucciones
    '''
    instrucciones = t[4] if t[4] is not None else []
    t[0] = Case(
        text_val = 'case',
        condicion = t[2],
        instrucciones = instrucciones,
        linea = t.lineno(1),
        columna = t.lexpos(1)
    )

#definimos la estructura de un default
def p_default_opcional(t):
    '''
    default_opcional : DEFAULT DOS_PUNTOS instrucciones
                     | 
    '''
    if len(t) > 1:
        t[0] = t[3]
    else:
        t[0] = []
def p_instruccion_if(t):
    ''' 
    instruccion_if : base_if
                   | base_if ELSE LLA instrucciones LLC
                   | base_if ELSE instruccion_if                 
    '''
    if len(t) == 2: # Solo base_if
        t[0] = t[1]
    elif len(t) == 6: # if con else
        t[0] = Instruccion_if(
            text_val=f'if ({t[1].condicion.text_val}) {{...}} else {{...}}',
            condicion=t[1].condicion,
            instrucciones_if=t[1].instrucciones_if,
            instrucciones_else=t[4],  # Lista de instrucciones del else
            linea=t.lineno(1),
            columna=t.lexpos(1)
        )
    else: # if con else if  
        t[0] = Instruccion_if(
            text_val=f'if ({t[1].condicion.text_val}) {{...}} else {t[3].text_val}',
            condicion=t[1].condicion,
            instrucciones_if=t[1].instrucciones_if,
            instrucciones_else=[t[3]],  # Otra instrucción if para el else if
            linea=t.lineno(1),
            columna=t.lexpos(1)
        )    
        

def p_base_if(t):
    ''' 
    base_if : IF PARA expresion PARC LLA instrucciones LLC
    '''
    text_val = f'if({t[3].text_val}) {{...}}'
    t[0] = Instruccion_if(
        text_val=text_val,
        condicion=t[3],
        instrucciones_if=t[6],
        instrucciones_else=None,  # Por ahora no hay else
        linea=t.lineno(1),
        columna=t.lexpos(1)
    )        


def p_incremento(t):
    '''
    incremento : ID INCREMENTO
    '''
    # Crear una expresión aritmética: id + 1
    acceso_var = Acceso(t[1], t[1], linea=t.lineno(1), columna=t.lexpos(1))
    literal_uno = Literal('1', TipoDato.INT, 1, t.lineno(1), t.lexpos(1))
    
    suma = Aritmetica(
        text_val=f'{t[1]} + 1',
        op1=acceso_var,
        operador=TipoAritmetica.SUMA,
        op2=literal_uno,
        linea=t.lineno(1),
        columna=t.lexpos(1)
    )
    
    # Crear asignación: id = (id + 1)
    text_val = f'{t[1]}++'
    t[0] = Asignacion(text_val, t[1], suma, t.lineno(1), t.lexpos(1))\
    
def p_decremento(t):
    '''
    decremento : ID DECREMENTO
    '''
    # Crear una expresión aritmética: id - 1
    acceso_var = Acceso(t[1], t[1], linea=t.lineno(1), columna=t.lexpos(1))
    literal_uno = Literal('1', TipoDato.INT, 1, t.lineno(1), t.lexpos(1))
    
    resta = Aritmetica(
        text_val=f'{t[1]} - 1',
        op1=acceso_var,
        operador=TipoAritmetica.RESTA,
        op2=literal_uno,
        linea=t.lineno(1),
        columna=t.lexpos(1)
    )
    
    # Crear asignación: id = (id - 1)
    text_val = f'{t[1]}--'
    t[0] = Asignacion(text_val, t[1], resta, t.lineno(1), t.lexpos(1))
    

def p_instruccion_println(t):
    'instruccion_println : PRINTLN PARA expresion PARC PYC'
    text_val = f'println({t[3].text_val})'
    t[0] = Print(text_val=text_val, argumento=t[3], linea=t.lineno(1), columna=t.lexpos(1))

def p_caracter(t):
    '''
    literal : CARACTER
    '''
    t[0] = Literal(f"'{t[1]}'", TipoDato.CHAR, t[1], t.lineno(1), t.lexpos(1))
    


def p_declaracion_variable(t):
    '''
    declaracion_variable : tipo ID IGUAL expresion
                        | tipo ID
    '''
    if len(t) == 5:  # tipo ID IGUAL expresion
        text_val = f'{tipoToStr(t[1])} {t[2]} = {t[4].text_val}'
        t[0] = Declaracion(text_val, t[2], t[1], t[4], t.lineno(1), t.lexpos(1))
    else:  # tipo ID (len(t) == 3)
        text_val = f'{tipoToStr(t[1])} {t[2]}'
        t[0] = Declaracion(text_val, t[2], t[1], None, t.lineno(1), t.lexpos(1))
    


def p_asignacion_variable(t):
    '''
    asignacion_variable : ID IGUAL expresion
    '''
    text_val = f'{t[1]} = {t[3].text_val}'
    t[0] = Asignacion(text_val, t[1], t[3], t.lineno(1), t.lexpos(1))

def p_literal_booleano(t):
    '''
    literal : TRUE
            | FALSE
    '''
    valor = True if t[1].lower() == 'true' else False
    t[0] = Literal(t[1], TipoDato.BOOL, valor, t.lineno(1), t.lexpos(1))

# Valores como tal. Eje. 123, "hola", var.
def p_expresion(t):
    '''
    expresion : aritmetica
              | literal
              | relacional

    '''
    t[0] = t[1]

def p_expresion_parentesis(t):
    'expresion : PARA expresion PARC'
    t[0] = t[2]

def p_expresion_nativa(t):
    ''' 
    expresion : SENO PARA expresion PARC
              | COSENO PARA expresion PARC
              | INV PARA expresion PARC
    '''
    func = t[1].upper() #t1 = seno
    args = t[3]  #t3 = expresion
    #SENO
    if func == 'SENO':
        t[0] = Seno(text_val=f'seno({args.text_val})', 
                    argumento=args, 
                    linea=t.lineno(1), 
                    columna=t.lexpos(1))
        
    elif func == 'COSENO':
        t[0] = Coseno(text_val=f'coseno({args.text_val})', 
                    argumento=args, 
                    linea=t.lineno(1), 
                    columna=t.lexpos(1))

    elif func == 'INV':
        t[0] = Inv(text_val=f'inv({args.text_val})', 
                    argumento=args, 
                    linea=t.lineno(1), 
                    columna=t.lexpos(1))


def p_expresion_aritmetica(t):
    '''
    aritmetica : expresion SUMA expresion
                | expresion RESTA expresion
                | expresion MULTIPLICACION expresion
                | expresion DIVISION expresion
                | expresion POTENCIA expresion
                | expresion MODULO expresion
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
    elif t[2] == '**':
        t[0] = Aritmetica(text_val=text_val,op1=t[1], operador=TipoAritmetica.POTENCIA, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))
    elif t[2] == '%':
        t[0] = Aritmetica(text_val=text_val,op1=t[1], operador=TipoAritmetica.MODULO, op2=t[3], linea=t.lineno(1), columna=t.lexpos(1))

def p_expresion_logica_binaria(t):
    '''
    expresion : expresion OR expresion
              | expresion AND expresion
              | expresion XOR expresion
    '''
    t[0] = Logica(t[1], t[3], t[2], t.lineno(2), t.lexpos(2))

def p_expresion_umenos(t):
    'expresion : RESTA expresion %prec UMENOS'
    t[0] = Aritmetica(
        text_val='-',
        op1=None,
        operador=TipoAritmetica.NEGACION,
        op2=t[2],  # <-- t[2] debe ser una expresión válida
        linea=t.lineno(1),
        columna=t.lexpos(1)
    )

def p_relacional(t):
    '''
    relacional : expresion IGUALACION expresion
               | expresion DIFERENCIACION expresion
               | expresion MENOR expresion
               | expresion MAYOR expresion
               | expresion MENOR_IGUAL expresion
               | expresion MAYOR_IGUAL expresion
    '''
    text_val = f'{t[1].text_val} {t[2]} {t[3].text_val}'
    if t[2] == '==':
        t[0] = Relacional(t[1], t[3], TipoRelacional.IGUALACION, t.lineno(1), t.lexpos(1))
    elif t[2] == '!=':
        t[0] = Relacional(t[1], t[3], TipoRelacional.DIFERENCIACION, t.lineno(1), t.lexpos(1))
    elif t[2] == '<':
        t[0] = Relacional(t[1], t[3], TipoRelacional.MENOR, t.lineno(1), t.lexpos(1))
    elif t[2] == '>':
        t[0] = Relacional(t[1], t[3], TipoRelacional.MAYOR, t.lineno(1), t.lexpos(1))
    elif t[2] == '<=':
        t[0] = Relacional(t[1], t[3], TipoRelacional.MENOR_IGUAL, t.lineno(1), t.lexpos(1))
    elif t[2] == '>=':
        t[0] = Relacional(t[1], t[3], TipoRelacional.MAYOR_IGUAL, t.lineno(1), t.lexpos(1))

#expresion not unario
def p_expresion_not(t):
    'expresion : NOT expresion %prec NOT'
    # Solo derecha, izquierda es None
    t[0] = Logica(None, t[2], '!', t.lineno(1), t.lexpos(1))

def p_entero(t):
    '''
    literal : ENTERO
    '''
    #t[0] = Literal(t[1], TipoDato.INT, int(t[1]), t.lineno(1), t.lexpos(1))
    t[0] = Literal('', TipoDato.INT, t[1], t.lineno(1), find_column(t.lexer.lexdata, t.slice[1]))

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
        | BOOL
    '''
    if(t[1] == 'int'):
        t[0] = TipoDato.INT;
    elif(t[1] == 'float'):
        t[0] = TipoDato.FLOAT;
    elif(t[1] == 'char'):
        t[0] = TipoDato.CHAR;
    elif(t[1] == 'bool'):
        t[0] = TipoDato.BOOL;
    elif(t[1] == 'str'):
        if len(t) == 2:
            t[0] = TipoDato.STR
        else:
            text_val = f'STR({t[3].text_val})'
            t[0] = TipoChars(text_val, TipoDato.STR, t[2]);

# Declaración de instrucciones adicionales de break y continue
def p_instruccion_break(t):
    'instruccion : BREAK PYC'
    t[0] = Break('break', t.lineno(1), t.lexpos(1))

def p_instruccion_continue(t):
    'instruccion : CONTINUE PYC'
    t[0] = Continue('continue', t.lineno(1), t.lexpos(1))


def p_declaracion_variable_error(t):
    'declaracion_variable : ID ID'
    # No hacer nada, solo sincronizar
    t[0] = None

# Error sintáctico
def p_error(t):
    if t is not None:
        err = Error(
            tipo='Sintáctico',
            linea=t.lineno,
            columna=find_column(t.lexer.lexdata, t),
            descripcion=f'No se esperaba token: {t.value}'
        )
        TablaErrores.addError(err)
        
        print(f"DEBUG: Error sintáctico en '{t.value}' línea {t.lineno}")
        
        # Estrategia simple: saltar el token problemático
        parser.errok()
        
    else:
        err = Error(
            tipo='Sintáctico',
            linea=0,
            columna=0,
            descripcion='Final inesperado del archivo'
        )
        TablaErrores.addError(err)

# Build the parser
parser = yacc(debug=True)
