from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato
from .expresion import Expresion
from interprete.otros.retorno import Retorno
from interprete.otros.enviroment import Enviroment
from interprete.instrucciones.instruccion import Instruccion

#Define el analisis de las secuencias de escape y el tipo de dato del literal.
class Literal(Expresion):
    def __init__(self, text_val:str, tipo, valor, linea:int, columna:int):
        super().__init__(text_val, linea, columna)
        self.valor = valor
        self.tipo = tipo
    
    def ejecutar(self, env:Enviroment):
        if self.tipo == TipoDato.STR or self.tipo == TipoDato.CHAR:
            self.valor = self.valor.replace("\\n", "\n").replace("\\\\", "\\").replace("\\r", "\r").replace("\\t", "\t").replace("\\\"", "\"").replace("\\\'", "\'").replace("\"", "").replace("\'", "")
            
        return Retorno(tipo=self.tipo, valor=self.valor)
       
    def recorrerArbol(self, raiz:Nodo):
        id = AST.generarId()
        hijo = Nodo(id=id, valor=self.valor, hijos=[])
        raiz.addHijo(hijo)