import ply.lex as lex

from interprete.otros.errores import *

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
    #'id': 'ID',
    'else': 'ELSE',
    'switch': 'SWITCH',
    'case': 'CASE',
    'default': 'DEFAULT',
    'while': 'WHILE',
    'for': 'FOR',
    'break': 'BREAK',
    #'print': 'PRINT',
    'println': 'PRINTLN',
    'return': 'RETURN',
    'continue': 'CONTINUE',
    'var': 'VAR',
    'do': 'DO',
    'seno': 'SENO',
    'coseno': 'COSENO',
    'inv': 'INV',
    'vector': 'VECTOR',
    'shuffle': 'SHUFFLE',
    'sort': 'SORT',
    'proc': 'PROC',        
    'exec': 'EXEC', 
}

# Lista de tokens
tokens = [
    'ID',
    'ENTERO',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'MODULO',
    'POTENCIA',
    'DIVISION',
    'DECIMAL',
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
    'DOS_PUNTOS',
    'ARROBA',
    'COMA',
    'LLA',
    'LLC',
    'UMENOS',
    'INCREMENTO',
    'DECREMENTO',
    'CORCHETE_ABRE',
    'CORCHETE_CIERRA'
] + list(reservadas.values())

# Expresiones regulares para tokens simples
t_SUMA = r'\+'
t_RESTA = r'-'
t_POTENCIA = r'\*\*'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
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
t_DOS_PUNTOS = r':'
t_ARROBA = r'@'
t_COMA = r','
t_LLA = r'\{'
t_LLC = r'\}'
t_INCREMENTO = r'\+\+'
t_DECREMENTO = r'--'
t_CORCHETE_ABRE = r'\[' 
t_CORCHETE_CIERRA = r'\]'

# Expresiones regulares para comentarios
def t_COMENTARIO_UNA_LINEA(t):
    r'//.*'
    pass

def t_COMENTARIO_MULTILINEA(t):
    r'[/][*][^*]*[*]+([^/*][^*]*[*]+)*[/]'
    t.value = t.value[2:-2].replace('\n', ' ')  # Eliminar los delimitadores de comentario
    pass

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
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Elimina las comillas dobles
    return t

# Regla para booleanos
#def t_BOOLEANO(t):
 #   r'\b(true|false)\b'
  #  t.value = (t.value == 'true')  # Convertir a booleano
   # return t

# Regla para caracteres
def t_CARACTER(t):
    r"'(\\.|[^\\'])'"
    t.value = t.value[1:-1]  # Remueve las comillas simples
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t_lower = t.value.lower()
    t.type = reservadas.get(t_lower, 'ID')  # Para el case insensitive
    t.value = t_lower  # <-- Esto hace que el valor sea siempre minúscula
    return t

  # Incrementa el número de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    # NO RETURN - correcto para saltos de línea

# Mover esta función ANTES de t_ignore
t_ignore = ' \t'  # Quitar \r\n de aquí ya que se maneja en t_newline

# Manejo de errores
def t_error(t):
    # Agregando a la tabla de erorres
    err = Error(tipo='Léxico', linea=t.lexer.lineno, columna=find_column(t.lexer.lexdata, t), descripcion=f'Caracter no reconocido: {t.value[0]}')
    TablaErrores.addError(err)
    t.lexer.skip(1)

def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos + 1) + 1
    return (token.lexpos - line_start) + 1

def t_eof(t):  #end of file
    t.lexer.lineno = 0
    
lexer = lex.lex()