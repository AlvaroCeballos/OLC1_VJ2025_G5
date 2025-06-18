from interprete.instrucciones.instruccion import Instruccion
from interprete.otros.errores import Error, TablaErrores

class Continue(Instruccion):
    def __init__(self, text_val, linea, columna):
        super().__init__(text_val, linea, columna)

    def ejecutar(self, env):
        # Verifica si está dentro de un ciclo
        entorno = env
        while entorno is not None:
            if entorno.nombre in ['for', 'while', 'do-while']:
                return 'continue'
            entorno = entorno.ent_anterior        # Si no está en ciclo, error
        TablaErrores.addError(Error(
            tipo='Semántico',
            linea=self.linea,
            columna=self.columna,
            descripcion='La sentencia continue solo puede usarse dentro de un ciclo.'
        ))
        return None
    
    def recorrerArbol(self, raiz):
        pass