from interprete.otros.symbol import Symbol
from interprete.otros.tipos import TipoSimbolo
from interprete.otros.symbol_table import TablaSimbolos

class Enviroment():
    env_list = []
    def __init__(self, ent_anterior, ambito:str):
        self.ent_anterior:Enviroment = ent_anterior
        self.ambito = ambito
        self.ts_variables = TablaSimbolos()
        self.ts_funciones = TablaSimbolos() # Se define tabla de simbolos para funciones para la fase 2
        self.dentro_funcion = False
        self.tamanio = 0                    # Para manejo de funciones/procedimientos (es como un offset)
        Enviroment.addEnviroment(self)