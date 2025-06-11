import ply.yacc as yacc
from lexer import tokens

# Tabla de símbolos para almacenar variables
tablaSimbolos = {}

# Función auxiliar para manejar variables
def nuevaVariableTS(nombre, tipo, valor):
    # Normalizar el tipo a minúsculas (o mayúsculas, según prefieras)
    tipo_normalizado = tipo.lower()
    tablaSimbolos[nombre] = {'tipo': tipo_normalizado, 'valor': valor}
    return tablaSimbolos[nombre]

def actualizarVariableTS(nombre, valor):
    if nombre in tablaSimbolos:
        tablaSimbolos[nombre]['valor'] = valor
        return tablaSimbolos[nombre]
    else:
        print(f"Error: Variable '{nombre}' no ha sido declarada")
        return None

# Se definen precedencias y asociaciones de operadores
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

# GRAMÁTICA -------------------------

# Producción inicial para generar AST
def p_programa(t):
    'programa : instrucciones'
    t[0] = t[1]

# Producción para lista de instrucciones (recursiva por derecha)
def p_instrucciones_lista(t):
    '''instrucciones    : instruccion instrucciones
                        | instruccion '''
    
    # Se asigna que si vienen 3 elementos, instrucciones será la suma de alguna instrucción anterior y otra lista de instrucciones
    if len(t) == 3:
        t[0] = [t[1]] + t[2]
    # Caso contrario, solamente se asigna la instrucción individual que venga
    else:
        t[0] = [t[1]]

# Producción para la instrucción en sí
def p_instruccion(t):
    '''instruccion : declaracion_variable
                   | asignacion
                   | otras_instrucciones'''
    t[0] = t[1]

# Servirá para manejar otras instrucciones más tarde
def p_otras_instrucciones(t):
    '''otras_instrucciones : '''
    t[0] = None

# Para la declaración de variables
def p_declaracion_variable(t):
    '''declaracion_variable : tipo ID IGUAL expresion PYC
                        | tipo ID PYC'''
                           
    if len(t) == 6:  # Con inicialización: tipo ID = expresion ;
        print(f'Declaración de variable: {t[2]} de tipo {t[1]} con valor {t[4]}')
        variable = nuevaVariableTS(t[2], t[1], t[4])
    else:  # Sin inicialización: tipo ID ;
        print(f'Declaración de variable: {t[2]} de tipo {t[1]} sin valor inicial')
        # Asignamos None (null) como valor por defecto
        variable = nuevaVariableTS(t[2], t[1], None)
    
    t[0] = variable

# Producción para asignación a variables existentes
def p_asignacion_variable(t):
    'asignacion : ID IGUAL expresion PYC'
    print(f'Asignación a variable: {t[1]} con nuevo valor {t[3]}')
    variable = actualizarVariableTS(t[1], t[3])
    t[0] = variable

# Para negación de expresiones
def p_expresion_umenos(t):
    'expresion : RESTA expresion %prec UMENOS'
    t[0] = -t[2]

# Producción para tipos de datos
def p_tipo(t):
    '''tipo : INT
            | FLOAT
            | BOOL
            | CHAR
            | STR'''
    t[0] = t[1]

# Expresiones simples de un dígito
def p_expresion_entero(t):
    'expresion : ENTERO'
    t[0] = t[1]

# Manejo de errores sintácticos simples
def p_error(t):
    if t:
        print(f"Error sintáctico en '{t.value}'")
    else:
        print("Error sintáctico al final del archivo")

# Construir parser
def build_parser():
    return yacc.yacc()