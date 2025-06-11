from lexer import build_lexer
from parserG import build_parser

def main():
    # Construir analizadores
    lexer = build_lexer()
    parser = build_parser()
    
    # Leer archivo de entrada
    input_file = "C:/Users/aceba/Downloads/OLC1_VJ2025-main/OLC1_VJ2025-main/Clase1/entrada.txt"
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = f.read()
        
        # Realizar análisis léxico
        lexer.input(data)
        
        # Opcional: mostrar tokens encontrados
        # for token in lexer:
        #     print(f"Token: {token.type}, Valor: {token.value}")
        
        # Realizar análisis sintáctico
        result = parser.parse(data, lexer=lexer)
        
        # Mostrar resultado
        print("Resultado del análisis:", result)
        
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{input_file}'")
    except Exception as e:
        print(f"Error al analizar el archivo: {e}")

if __name__ == "__main__":
    main()