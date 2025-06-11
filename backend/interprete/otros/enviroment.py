from interprete.otros.symbol import Symbol
from interprete.otros.tipos import TipoSimbolo
from interprete.otros.symbol_table import TablaSimbolos

class Enviroment():
    env_list = []
    def __init__(self, ent_anterior, ambito:str):
        self.ent_anterior:Enviroment = ent_anterior # Entorno anterior, para poder hacer el manejo de variables globales y locales
        self.ambito = ambito # Ambito del entorno, puede ser global o local
        self.ts_variables = TablaSimbolos()
        self.ts_funciones = TablaSimbolos() # Se define tabla de simbolos para funciones para la fase 2
        self.dentro_funcion = False
        self.tamanio = 0                    # Para manejo de funciones/procedimientos (es como un offset)
        Enviroment.addEnviroment(self)

        # Incrementa el tamaño del entorno
    def incrementarTamanio(self):
        self.tamanio += 1

    def getTamanio(self):
        return self.tamanio

    def insertar_simbolo(self, id:str, simbolo:Symbol):
        if simbolo.tipo_simbolo == TipoSimbolo.VARIABLE:
            self.ts_variables.instertarSimbolo(id, simbolo)
        elif simbolo.tipo_simbolo == TipoSimbolo.FUNCTION:
            self.ts_funciones.instertarSimbolo(id, simbolo)