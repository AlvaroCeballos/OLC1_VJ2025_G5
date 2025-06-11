from interprete.otros.enviroment import Enviroment
from .expresion import Expresion
from interprete.expresiones.literal import Literal
from interprete.otros.tipos import *
from interprete.otros.enviroment import Enviroment

class TipoChars(Expresion):
    def __init__(self, text_val:int,charTipo:TipoDato, valor:Literal):
        self.text_val = text_val
        self.charTipo = charTipo
        self.valor = valor
        
    def ejecutar(self, env:Enviroment):
        return self.valor.ejecutar(env)