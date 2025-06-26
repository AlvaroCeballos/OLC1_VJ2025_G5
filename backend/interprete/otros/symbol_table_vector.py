class TablaSimbolosVector:
    def __init__(self):
        self.ts_vectores = {}
        
    def insertarVector(self, id: str, simbolo):
        """Inserta un vector en la tabla"""
        self.ts_vectores[id] = simbolo
    
    def buscarVector(self, id: str):
        """Busca un vector por ID"""
        return self.ts_vectores.get(id)

    def getVector(self, id: str):
        """Obtiene un vector por ID"""
        return self.ts_vectores.get(id)
    
    def getTSVectores(self):
        """Retorna todos los vectores"""
        return self.ts_vectores.values()
    
    def existeVector(self, id: str) -> bool:
        """Verifica si existe un vector"""
        return id in self.ts_vectores
    
    def eliminarVector(self, id: str):
        """Elimina un vector de la tabla"""
        if id in self.ts_vectores:
            del self.ts_vectores[id]
    
    def limpiarTabla(self):
        """Limpia toda la tabla de vectores"""
        self.ts_vectores.clear()
    
    def getTablaComoLista(self):
        """Retorna la tabla como lista de diccionarios para JSON"""
        return [vector.toDict() for vector in self.ts_vectores.values()]