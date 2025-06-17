from interprete.otros.enviroment import Enviroment
from .instruccion import Instruccion
from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato


class Break(Instruccion):

    def __init__(self, text_val :str, linea :int, columna :int):
        super().__init__(text_val, linea, columna)

    def ejecutar(self, env: Enviroment):
        return 'break'
    
    def recorrerArbol(self, raiz):
        id_break = AST.generarId()
        nodo_break = Nodo(id=id_break, valor='BREAK', hijos=[])
        raiz.addHijo(nodo_break)