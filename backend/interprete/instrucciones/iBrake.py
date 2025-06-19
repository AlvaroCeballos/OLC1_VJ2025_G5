from interprete.otros.enviroment import Enviroment
from .instruccion import Instruccion
from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato


class Break(Instruccion):

    def __init__(self, text_val :str, linea :int, columna :int):
        super().__init__(text_val, linea, columna)

    def ejecutar(self, env):
        # Verifica si está dentro de un ciclo o switch
        entorno = env
        while entorno is not None:
            if entorno.nombre in ['for', 'while', 'dowhile', 'switch']:
                return 'break'
            entorno = entorno.ent_anterior
        TablaErrores.addError(Error(
            tipo='Semántico',
            linea=self.linea,
            columna=self.columna,
            descripcion='La sentencia break solo puede usarse dentro de un ciclo o switch.'
        ))
        return None
    
    def recorrerArbol(self, raiz):
        pass