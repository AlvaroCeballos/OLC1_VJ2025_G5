from analizadores import lexer
from analizadores import parser

# Leer el archivo
archivo = r"C:\Users\52338386\OneDrive - Conduent\Documents\Training\Ing\Compi1\OLC1_VJ2025_G5\OLC1_VJ2025_G5\backend\entrada.txt"

with open(archivo, 'r', encoding='utf-8') as f:
    input_text = f.read()

# Asignar el texto al lexer
lexer.lexer.input(input_text)

# Llamar al parser
resultado = parser.parser(input_text)

# Opcional: imprimir las instrucciones obtenidas
if resultado:
    for instruccion in resultado:
        print(f'Ejecutar: {instruccion.text_val}')