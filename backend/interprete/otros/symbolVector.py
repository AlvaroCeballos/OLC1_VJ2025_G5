from interprete.otros.tipos import *

class SymbolVector:
    def __init__(self, tipo_simbolo: TipoSimbolo = None, tipo: TipoDato = None, 
                 id: str = '', dimensiones: list = [], datos: list = [], 
                 tamanio_total: int = 0, ambito: str = ''):
        self.tipo_simbolo = tipo_simbolo        # TipoSimbolo.VECTOR
        self.tipo = tipo                        # TipoDato.INT, FLOAT, etc.
        self.id = id                           # Nombre del vector
        self.dimensiones = dimensiones         # [5] o [2,3] para matrices
        self.datos = datos                     # Lista lineal de datos
        self.tamanio_total = tamanio_total     # Tamaño total del vector
        self.ambito = ambito                   # Ámbito donde se declara

    def serializarDimensiones(self):
        """Convierte las dimensiones a string para reporte"""
        return str(self.dimensiones)
    
    def serializarDatos(self):
        """Convierte los datos a string para reporte (limitado)"""
        if len(self.datos) <= 10:
            return str(self.datos)
        else:
            return f"[{', '.join(map(str, self.datos[:5]))}, ..., {', '.join(map(str, self.datos[-5:]))}]"
    
    def toDict(self):
        """Convierte el símbolo a diccionario para JSON"""
        return {
            'simbolo': 'VECTOR',
            'tipo': self.tipo.name if self.tipo else 'UNKNOWN',
            'id': self.id,
            'dimensiones': self.dimensiones,
            'datos': self.datos,
            'tamanio_total': self.tamanio_total,
            'ambito': self.ambito
        }