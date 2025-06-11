from subprocess import check_call
from types import NoneType
from interprete.otros.errores import TablaErrores, Error
from interprete.otros.consola import Consola

class Nodo:
    # id -> Identificador del dodo
    # valor -> Contenido del nodo
    # hijos -> Arreglo de 'n' hijos
    def __init__(self, id, valor:str, hijos):
        self.id = id
        self.valor = valor
        self.hijos = hijos
    
    def addHijo(self, nodoHijo):
        self.hijos.append(nodoHijo)
    
    def getId(self):
        return self.id
    
    def getValor(self):
        return self.valor
    
    def getHijos(self):
        return self.hijos