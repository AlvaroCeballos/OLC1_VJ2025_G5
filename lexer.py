import ply.lex as lex

# Palabras reservadas
reservadas = {
    'int': 'INT',
    'float': 'FLOAT',
    'boolean': 'BOOLEAN',
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
    'DOS_PUNTOS',
    'ARROBA',
    'COMA',
    'LLA',
    'LLC'
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
t_DOS_PUNTOS = r':'
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
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t

# Reglas especiales
t_ignore = ' \t\r\n'  # Ignora espacios y tabulaciones

# Manejo de errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Leer desde archivo
with open("entrada.txt", "r", encoding="utf-8") as f:
    data = f.read()


lexer.input(data)

print("Tokens encontrados:")
for tok in lexer:
    print(tok)