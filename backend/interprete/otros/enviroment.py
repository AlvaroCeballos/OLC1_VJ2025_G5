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
        # Funcion para agregar un ssimbolo al entorno
    def insertar_simbolo(self, id:str, simbolo:Symbol):
        if simbolo.tipo_simbolo == TipoSimbolo.VARIABLE:
            self.ts_variables.instertarSimbolo(id, simbolo)
        elif simbolo.tipo_simbolo == TipoSimbolo.FUNCTION:
            self.ts_funciones.instertarSimbolo(id, simbolo)

        #Funcion para verificar si existe el simbolo
    def existe_simbolo(self, id:str, tipoSimbolo:TipoSimbolo):
        ent:Enviroment = self

        while ent is not None:
            if(tipoSimbolo == TipoSimbolo.VARIABLE):
                existe = ent.ts_variables.buscarSimbolo(id)

        #se busca dentro de la tabla de simbolos funciones
            elif(tipoSimbolo == TipoSimbolo.FUNCTION):
                existe = ent.ts_funciones.buscarSimbolo(id)
            if (existe is not None):
                return True
            ent = ent.ent_anterior
        return False
    
    #Se obtiene el simbolo del entorno actual o de los anteriores
    def getSimbolo(self, id:str, tipo_simbolo:TipoSimbolo):
        ent:Enviroment = self
        
        while ent is not None:
            if (tipo_simbolo == TipoSimbolo.VARIABLE):
                simbolo = ent.ts_variables.getSimbolo(id)
            elif (tipo_simbolo == TipoSimbolo.FUNCTION):
                simbolo = ent.ts_funciones.getSimbolo(id)
            if (simbolo is not None):
                return simbolo
            ent = ent.ent_anterior
        return None
    
    #Se obtiene el simbolo unicamente del entorno actual
    def existe_simbolo_ent_actual(self, id:str, tipo_simbolo:TipoSimbolo):
        if(tipo_simbolo == TipoSimbolo.VARIABLE):
            existe = self.ts_variables.getSimbolo(id)
        elif (tipo_simbolo == TipoSimbolo.FUNCTION):
            existe = self.ts_funciones.getSimbolo(id)
        if(existe is not None):
            return True
        return False
    
    def dentroDeFuncion(self) -> bool:
        ent:Enviroment = self
        
        while ent is not None:
            if ent.getDentroFunction():
                return True
            ent = ent.ent_anterior
        return False
    
    def setDentroFuncion(self, val:bool):
        self.dentro_funcion = val
    
    def getDentroFunction(self):
        return self.dentro_funcion