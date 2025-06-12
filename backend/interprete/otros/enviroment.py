from interprete.otros.symbol import Symbol
from interprete.otros.tipos import TipoSimbolo
from interprete.otros.symbol_table import TablaSimbolos

class Enviroment():
    env_list = []
    def __init__(self, ent_anterior, ambito:str):
        self.ent_anterior:Enviroment = ent_anterior
        self.ambito = ambito
        self.ts_variables = TablaSimbolos()
        self.ts_funciones = TablaSimbolos()
        self.dentro_funcion = False
        self.tamanio = 0                    # Para manejo de funciones/procedimientos (es como un offset)
        Enviroment.addEnviroment(self)
    
    # Incrementa el tamaño del entorno
    def incrementarTamanio(self):
        self.tamanio += 1

    def getTamanio(self):
        return self.tamanio

    # Inserta un simbolo en la tabla de simbolos del entorno actual
    def insertar_simbolo(self, id:str, simbolo:Symbol):
        #Validar si el simbolo es funcion o variable
        if simbolo.tipo_simbolo == TipoSimbolo.VARIABLE:
            self.ts_variables.instertarSimbolo(id, simbolo)
        #Valida si el simbolo es una funcion    
        elif simbolo.tipo_simbolo == TipoSimbolo.FUNCTION:
            self.ts_funciones.instertarSimbolo(id, simbolo)
    
    # Busca un simbolo en el entorno actual o en los entornos anteriores
    def existe_simbolo(self, id:str, tipoSimbolo:TipoSimbolo):
        ent:Enviroment = self
        while ent is not None:
            if(tipoSimbolo == TipoSimbolo.VARIABLE):
                existe = ent.ts_variables.buscarSimbolo(id)
            elif(tipoSimbolo == TipoSimbolo.FUNCTION):
                existe = ent.ts_funciones.buscarSimbolo(id)
            if (existe is not None):
                return True
            ent = ent.ent_anterior
        return False
    
    #Obtiene el simbolo sobre todos los entornos
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
    
    # Valida si un simbolo existe en el entorno actual
    def existe_simbolo_ent_actual(self, id:str, tipo_simbolo:TipoSimbolo):
        if(tipo_simbolo == TipoSimbolo.VARIABLE):
            existe = self.ts_variables.getSimbolo(id)
        elif (tipo_simbolo == TipoSimbolo.FUNCTION):
            existe = self.ts_funciones.getSimbolo(id)
        if(existe is not None):
            return True
        return False
    
    # Valida si hay una funcion en un entorno mas externo
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
    
    # Serializa la tabla de simbolos de un entorno y genera un arreglo en formato JSON
    def getTablaSimbolos(self):
        simbolos = []
        # Llenado de variables
        for simbolo in self.ts_variables.getTS():
            template = {
                'simbolo': simbolo.tipo_simbolo.name,
                'tipo': simbolo.tipo.name,
                'id': simbolo.id,
                'valor': simbolo.valor,
                'parametros': simbolo.serializarParametros(),
                'ambito': simbolo.ambito
            }
            simbolos.append(template)

        # Llenado de funciones
        for simbolo in self.ts_funciones.getTS():
            template = {
                'simbolo': simbolo.tipo_simbolo.name,
                'tipo': simbolo.tipo.name,
                'id': simbolo.id,
                'valor': '',
                'parametros': simbolo.serializarParametros(),
                'ambito': simbolo.ambito
            }
            simbolos.append(template)
                    
        return simbolos

    
    @classmethod
    def addEnviroment(cls, env):
        cls.env_list.append(env)
    
    @classmethod
    def getEnviroments(cls):
        return cls.env_list
    
    # Obtiene los simbolos de todos los entornos creados
    @classmethod
    def serializarTodosSimbolos(cls):
        simbolos = []
        for env in cls.env_list:
            simbolos = simbolos + env.getTablaSimbolos()
        return simbolos

    @classmethod
    def cleanEnviroments(cls):
        cls.env_list = []