from backend.analizadores import lexer
from backend.analizadores import parser

# Leer el archivo
with open('entrada.txt', 'r') as f:
    input_text = f.read()

# Asignar el texto al lexer
lexer.lexer.input(input_text)

# Llamar al parser
resultado = parser.parse(input_text)

# Opcional: imprimir las instrucciones obtenidas
if resultado:
    for instruccion in resultado:
        print(f'Ejecutar: {instruccion.text_val}')