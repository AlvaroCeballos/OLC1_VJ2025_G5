from interprete.otros.symbol import Symbol
from interprete.otros.symbol_table import TablaSimbolos
from interprete.otros.symbol_table_vector import TablaSimbolosVector
from interprete.otros.symbolVector import SymbolVector
from interprete.otros.tipos import TipoSimbolo

class Enviroment():
    env_list = []
    
    def __init__(self, ent_anterior, ambito: str, nombre: str = "Global"):
        self.ent_anterior: Enviroment = ent_anterior
        self.ambito = ambito
        self.nombre = nombre
        self.ts_variables = TablaSimbolos()
        self.ts_funciones = TablaSimbolos()
        self.ts_vectores = TablaSimbolosVector()  
        self.dentro_funcion = False
        self.tamanio = 0
        Enviroment.addEnviroment(self)
    
    def incrementarTamanio(self):
        self.tamanio += 1

    def getTamanio(self):
        return self.tamanio

    def insertar_simbolo(self, id: str, simbolo: Symbol):
        """Inserta símbolos normales (variables y funciones) - NO vectores"""
        if simbolo.tipo_simbolo == TipoSimbolo.VARIABLE:
            self.ts_variables.instertarSimbolo(id, simbolo)
        elif simbolo.tipo_simbolo == TipoSimbolo.FUNCTION:
            self.ts_funciones.instertarSimbolo(id, simbolo)
        # Los vectores ya NO se insertan aquí
    
    def insertar_vector(self, id: str, simbolo_vector: SymbolVector):
        """Inserta vectores en su tabla específica"""
        self.ts_vectores.insertarVector(id, simbolo_vector)
    
    def existe_simbolo(self, id: str, tipoSimbolo: TipoSimbolo):
        """Busca símbolos en todos los entornos"""
        ent: Enviroment = self
        while ent is not None:
            if tipoSimbolo == TipoSimbolo.VARIABLE:
                existe = ent.ts_variables.buscarSimbolo(id)
            elif tipoSimbolo == TipoSimbolo.FUNCTION:
                existe = ent.ts_funciones.buscarSimbolo(id)
            elif tipoSimbolo == TipoSimbolo.VECTOR:
                existe = ent.ts_vectores.existeVector(id)
                if existe:
                    return True
                ent = ent.ent_anterior
                continue
            
            if existe is not None:
                return True
            ent = ent.ent_anterior
        return False

    def getSimbolo(self, id: str, tipo_simbolo: TipoSimbolo):
        """Obtiene símbolos de todos los entornos"""
        ent: Enviroment = self
        
        while ent is not None:
            if tipo_simbolo is None:
                # Buscar primero en variables
                simbolo = ent.ts_variables.getSimbolo(id)
                if simbolo is not None:
                    return simbolo
                # Buscar en funciones
                simbolo = ent.ts_funciones.getSimbolo(id)
                if simbolo is not None:
                    return simbolo
                # Buscar en vectores y convertir a Symbol
                vector = ent.ts_vectores.getVector(id)
                if vector is not None:
                    return self._convertir_vector_a_symbol(vector)
                    
            elif tipo_simbolo == TipoSimbolo.VARIABLE:
                simbolo = ent.ts_variables.getSimbolo(id)
                if simbolo is not None:
                    return simbolo
                    
            elif tipo_simbolo == TipoSimbolo.VECTOR:
                vector = ent.ts_vectores.getVector(id)
                if vector is not None:
                    return self._convertir_vector_a_symbol(vector)
                    
            elif tipo_simbolo == TipoSimbolo.FUNCTION:
                simbolo = ent.ts_funciones.getSimbolo(id)
                if simbolo is not None:
                    return simbolo
            
            ent = ent.ent_anterior
        return None
    
    def _convertir_vector_a_symbol(self, vector: SymbolVector) -> Symbol:
        """Convierte SymbolVector a Symbol para compatibilidad"""
        return Symbol(
            tipo_simbolo=TipoSimbolo.VECTOR,
            tipo=vector.tipo,
            id=vector.id,
            valor={
                'dimensiones': vector.dimensiones,
                'datos': vector.datos,
                'tamanio_total': vector.tamanio_total
            },
            ambito=vector.ambito,
            parametros=[],
            instrucciones=[],
            direccion=''
        )
    
    def existe_simbolo_ent_actual(self, id: str, tipo_simbolo: TipoSimbolo):
        """Valida si un símbolo existe en el entorno actual"""
        if tipo_simbolo == TipoSimbolo.VARIABLE:
            existe = self.ts_variables.getSimbolo(id)
        elif tipo_simbolo == TipoSimbolo.FUNCTION:
            existe = self.ts_funciones.getSimbolo(id)
        elif tipo_simbolo == TipoSimbolo.VECTOR:
            return self.ts_vectores.existeVector(id)
        
        if existe is not None:
            return True
        return False
    
    def dentroDeFuncion(self) -> bool:
        ent: Enviroment = self
        while ent is not None:
            if ent.getDentroFunction():
                return True
            ent = ent.ent_anterior
        return False
    
    def setDentroFuncion(self, val: bool):
        self.dentro_funcion = val
    
    def getDentroFunction(self):
        return self.dentro_funcion
    
    def getTablaSimbolos(self):
        """Serializa SOLO variables y funciones (sin vectores)"""
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
    
    def getTablaVectores(self):
        """Serializa SOLO vectores"""
        return self.ts_vectores.getTablaComoLista()
    
    @classmethod
    def addEnviroment(cls, env):
        cls.env_list.append(env)
    
    @classmethod
    def getEnviroments(cls):
        return cls.env_list
    
    @classmethod
    def serializarTodosSimbolos(cls):
        """Obtiene SOLO variables y funciones de todos los entornos"""
        simbolos = []
        for env in cls.env_list:
            simbolos = simbolos + env.getTablaSimbolos()
        return simbolos
    
    @classmethod
    def serializarTodosVectores(cls):
        """Obtiene SOLO vectores de todos los entornos"""
        vectores = []
        for env in cls.env_list:
            vectores = vectores + env.getTablaVectores()
        return vectores

    @classmethod
    def cleanEnviroments(cls):
        """Limpia todos los entornos incluyendo vectores"""
        for env in cls.env_list:
            env.ts_vectores.limpiarTabla()
        cls.env_list = []