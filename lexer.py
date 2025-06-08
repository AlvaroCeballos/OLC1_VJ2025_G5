import ply.lex as lex
import ply.yacc as yacc

# Palabras reservadas
reservadas = {
    'int': 'INT',
    'float': 'FLOAT',
    'bool': 'BOOL',
    'char': 'CHAR',
    'str': 'STR',
    'if': 'IF',
    'true': 'TRUE',
    'false': 'FALSE',
    'id': 'ID',
    'else': 'ELSE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'while': 'WHILE',
    'for': 'FOR',
    'break': 'BREAK',
    'do-while': 'DO_WHILE',
    'print': 'PRINT',
    'println': 'PRINTLN',
    'return': 'RETURN',
    'continue': 'CONTINUE',
    'var': 'VAR',
    'do': 'DO',
}


# Lista de tokens
tokens = [
    'ENTERO',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'MODULO',
    'POTENCIA',
    'DIVISION',
    'DECIMAL',
    'BOOLEANO',
    'CADENAS',
    'CARACTER',
    'COMENTARIO_UNA_LINEA',
    'COMENTARIO_MULTILINEA',
    'IGUALACION',
    'DIFERENCIACION',
    'MENOR',
    'MENOR_IGUAL',
    'MAYOR',
    'MAYOR_IGUAL',
    'IDENTIFICADOR',
    'IGUAL',
    'OR',
    'AND',
    'XOR',
    'NOT',
    'PARA',
    'PARC',
    'PYC',
    'ARROBA',
    'COMA',
    'LLA',
    'LLC',
    'UMENOS',
] + list(reservadas.values())


# Expresiones regulares para tokens simples
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_POTENCIA = r'\^'
t_MODULO = r'%'
t_IGUALACION = r'=='
t_DIFERENCIACION = r'!='
t_MENOR = r'<'
t_MENOR_IGUAL = r'<='
t_MAYOR = r'>'
t_MAYOR_IGUAL = r'>='
t_IGUAL = r'='
t_OR = r'\|\|'
t_AND = r'&&'
t_XOR = r'\^'
t_NOT = r'!'
t_PARA = r'\('
t_PARC = r'\)'
t_PYC = r';'
t_ARROBA = r'@'
t_COMA = r','
t_LLA = r'\{'
t_LLC = r'\}'

# Expresiones regulares para comentarios

def t_COMENTARIO_UNA_LINEA(t):
    r'//.*'
    t.value = t.value[2:]  # Eliminar el prefijo de comentario
    return t

def t_COMENTARIO_MULTILINEA(t):
    r'[/][*][^*]*[*]+([^/*][^*]*[*]+)*[/]'
    t.value = t.value[2:-2].replace('\n', ' ')  # Eliminar los delimitadores de comentario
    return t

 # Regla para números decimales
def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Regla para números
def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para cadenas de texto
def t_CADENAS(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]  # Eliminar comillas
    return t

# Regla para booleanos
def t_BOOLEANO(t):
    r'\b(true|false)\b'
    t.value = (t.value == 'true')  # Convertir a booleano
    return t

#Regla para caracteres
def t_CARACTER(t):
    r"'(\\.|[^\\'])'"
    t.value = t.value[1:-1]  # Remueve las comillas simples
    return t

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Cpara el case in sensitive
     return t

# Reglas especiales
t_ignore = ' \t\r\n'  # Ignora espacios y tabulaciones

# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


# Tabla de símbolos para almacenar variables
tablaSimbolos = {}

# Función auxiliar para manejar variables
def nuevaVariableTS(nombre, tipo, valor):
    tablaSimbolos[nombre] = {'tipo': tipo, 'valor': valor}
    return tablaSimbolos[nombre]

def actualizarVariableTS(nombre, valor):
    if nombre in tablaSimbolos:
        tablaSimbolos[nombre]['valor'] = valor
        return tablaSimbolos[nombre]
    else:
        print(f"Error: Variable '{nombre}' no ha sido declarada")
        return None

#se definen precedencias y asociaciones de operadores iniciales (aun no terminados)
precedence= (
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
# GRAMATICA-------------------------

#produccion inicial para generar AST
def p_programa(t):
    'programa : instrucciones'
    t[0] = t[1]

# Producción para lista de instrucciones (recursiva por derecha)
def p_instrucciones_lista(t):
    '''instrucciones    : instruccion instrucciones
                        | instruccion '''
    
    #Se asigna que si vienen 3 elementos, instrucciones sera la suma de alguna instrucción anterior y otra lista de instrucciones
    if len(t) == 3:
        t[0] = [t[1]] + t[2]
        #caso contrario, solamente se asigna la instruccion individual que venga
    else:
        t[0] = [t[1]]

# Producción para la instruccion en si
def p_instruccion(t):
    '''instruccion : declaracion_variable
                   | asignacion
                   | otras_instrucciones'''
    t[0] = t[1]

# Servirá para manejar otras instrucciones mas tarde
def p_otras_instrucciones(t):
    '''otras_instrucciones : '''
    t[0] = None

# Para la declaracion de variables
def p_declaracion_variable(t):
    'declaracion_variable : tipo ID IGUAL expresion PYC'
    print(f'Declaración de variable: {t[2]} de tipo {t[1]} con valor {t[4]}')
    variable = nuevaVariableTS(t[2], t[1], t[4])
    t[0] = variable

# Producción para asignación a variables existentes
def p_asignacion_variable(t):
    'asignacion : ID IGUAL expresion PYC'
    print(f'Asignación a variable: {t[1]} con nuevo valor {t[3]}')
    variable = actualizarVariableTS(t[1], t[3])
    t[0] = variable

#Para negación de expresiones
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

# Expresiones simples de un digito
def p_expresion_entero(t):
    'expresion : ENTERO'
    t[0] = t[1]

# Manejo de errores sintácticos simples
def p_error(t):
    if t:
        print(f"Error sintáctico en '{t.value}'")
    else:
        print("Error sintáctico al final del archivo")

# Se contruye parser con ply (analizador sintáctico)
parser = yacc.yacc()

# Se construye el analizador léxico con ply
lexer = lex.lex()

# Se lee archivo desde mi ruta (modificar mientras aun no tenemos carga de archivos)
with open("C:/Users/aceba/Downloads/OLC1_VJ2025-main/OLC1_VJ2025-main/Clase1/entrada.txt", "r", encoding="utf-8") as f:
    data = f.read()

lexer.input(data)

# Análisis léxico y sintáctico
result = parser.parse(data, lexer=lexer)
print("Resultado del análisis:", result)