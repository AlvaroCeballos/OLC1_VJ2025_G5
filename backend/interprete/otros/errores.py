#Se crea clase Error para manejar errores en el intérprete
class Error:
    def __init__(self, tipo:str, linea:int, columna:int, descripcion:str):
        self.tipo = tipo
        self.linea = linea
        self.columna = columna
        self.descripcion = descripcion

    def serializar(self):
        return {
            'tipo': self.tipo,
            'linea': self.linea,
            'columna': self.columna,
            'descripcion': self.descripcion
        }