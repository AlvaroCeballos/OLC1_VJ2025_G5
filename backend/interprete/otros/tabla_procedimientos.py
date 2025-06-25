


class TablaProcedimientos:
    procedimientos = {}
    
    @staticmethod
    def agregar(procedimiento):
        TablaProcedimientos.procedimientos[procedimiento.id] = procedimiento
    @staticmethod
    def existe(id):
        return id in TablaProcedimientos.procedimientos
    @staticmethod
    def obtener(id):
        return TablaProcedimientos.procedimientos.get(id,None)
    @staticmethod
    def limpiar():
        TablaProcedimientos.procedimientos.clear()

