from interprete.otros.enviroment import Enviroment
from .instruccion import Instruccion
from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato

class Case(Instruccion):

    def __init__(self, text_val: str, condicion, instrucciones, linea: int, columna: int):
        super().__init__(text_val, linea, columna)
        self.condicion = condicion
        self.instrucciones = instrucciones if instrucciones is not None else []

    def ejecutar(self, env: Enviroment):
        #condicion del case
        for instruccion in self.instrucciones:
            resultado = instruccion.ejecutar(env)
            if resultado == 'break':
                return 'break'
            
    def recorrerArbol(self, raiz):
        id_case = AST.generarId()
        nodo_case = Nodo(id=id_case, valor='CASE', hijos=[])
        raiz.addHijo(nodo_case)

        # Nodo de la condición del case
        id_cond = AST.generarId()
        nodo_cond = Nodo(id=id_cond, valor='CONDICION', hijos=[])
        nodo_case.addHijo(nodo_cond)
        self.condicion.recorrerArbol(nodo_cond)

        # Nodos de las instrucciones del case
        id_instr = AST.generarId()
        nodo_instr = Nodo(id=id_instr, valor='INSTRUCCIONES', hijos=[])
        nodo_case.addHijo(nodo_instr)
        for instruccion in self.instrucciones:
            instruccion.recorrerArbol(nodo_instr)
            
