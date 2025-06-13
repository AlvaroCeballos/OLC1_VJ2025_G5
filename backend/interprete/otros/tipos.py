from enum import Enum

class TipoDato(Enum):
    INT = 1
    FLOAT = 2
    BOOLEAN = 3
    CHAR = 4
    STR = 5
    NULL = 6
    ERROR = 7
    UNDEFINED = 8

class TipoAritmetica(Enum):
    SUMA = 1
    RESTA = 2
    MULTIPLICACION = 3
    DIVISION = 4
    POTENCIA = 5
    MODULO = 6
    NEGACION = 7

class TipoRelacional(Enum):
    IGUALACION = 1
    DIFERENCIACION = 2
    MENOR_IGUAL = 3
    MAYOR_IGUAL = 4
    MENOR = 5
    MAYOR = 6
    IGUAL = 7

class TipoLogico(Enum):
    NOT = 1
    XOR = 2
    AND = 3
    OR = 4

class TipoSimbolo(Enum):
    VARIABLE = 1
    FUNCTION = 2