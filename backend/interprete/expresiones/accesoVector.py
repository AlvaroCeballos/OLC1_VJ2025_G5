# archivo: backend/interprete/expresiones/accesoVector.py
from interprete.otros.ast import *
from interprete.expresiones.expresion import Expresion
from interprete.otros.tipos import TipoDato, TipoSimbolo
from interprete.otros.retorno import Retorno
from interprete.otros.errores import Error, TablaErrores

class AccesoVector(Expresion):
    def __init__(self, id_vector, indices, linea, columna):
        super().__init__('', linea, columna)
        self.id_vector = id_vector
        self.indices = indices  # Lista de expresiones para los índices
        self.text_val = f'{id_vector}[{"][".join([idx.text_val for idx in indices])}]'
    
    def ejecutar(self, env):
        # Buscar el vector en la tabla de símbolos
        simbolo = env.getSimbolo(self.id_vector, TipoSimbolo.VECTOR)
        if simbolo is None:
            TablaErrores.addError(Error('Semántico', self.linea, self.columna, 
                                      f'No existe un vector con el nombre {self.id_vector}'))
            return Retorno(tipo=TipoDato.ERROR, valor=None)
        
        # Evaluar los índices
        indices_evaluados = []
        for idx_expr in self.indices:
            resultado = idx_expr.ejecutar(env)
            if resultado.tipo != TipoDato.INT:
                TablaErrores.addError(Error('Semántico', self.linea, self.columna, 
                                          'Los índices del vector deben ser enteros'))
                return Retorno(tipo=TipoDato.ERROR, valor=None)
            indices_evaluados.append(resultado.valor)
        
        # Validar número de dimensiones
        dimensiones = simbolo.valor['dimensiones']
        if len(indices_evaluados) != len(dimensiones):
            TablaErrores.addError(Error('Semántico', self.linea, self.columna, 
                                      f'El vector tiene {len(dimensiones)} dimensiones, pero se proporcionaron {len(indices_evaluados)} índices'))
            return Retorno(tipo=TipoDato.ERROR, valor=None)
        
        # Validar rangos de índices
        for i, (indice, dimension) in enumerate(zip(indices_evaluados, dimensiones)):
            if indice < 0 or indice >= dimension:
                TablaErrores.addError(Error('Semántico', self.linea, self.columna, 
                                          f'Índice {indice} fuera de rango para la dimensión {i+1} (0-{dimension-1})'))
                return Retorno(tipo=TipoDato.ERROR, valor=None)
        
        # Calcular posición lineal
        posicion_lineal = self._calcular_posicion_lineal(indices_evaluados, dimensiones)
        
        # Obtener el valor
        datos = simbolo.valor['datos']
        valor = datos[posicion_lineal]
        
        return Retorno(tipo=simbolo.tipo, valor=valor)
    
    def _calcular_posicion_lineal(self, indices, dimensiones):
        """Convierte índices multidimensionales a posición lineal"""
        posicion = 0
        multiplicador = 1
        
        # Recorrer desde la última dimensión hacia atrás
        for i in range(len(indices) - 1, -1, -1):
            posicion += indices[i] * multiplicador
            if i > 0:
                multiplicador *= dimensiones[i]
        
        return posicion
    
    def recorrerArbol(self, raiz: Nodo):
        id_acceso = AST.generarId()
        nodo_acceso = Nodo(id=id_acceso, valor='ACCESO_VECTOR', hijos=[])
        raiz.addHijo(nodo_acceso)
        
        # ID del vector
        id_id = AST.generarId()
        nodo_id = Nodo(id=id_id, valor=self.id_vector, hijos=[])
        nodo_acceso.addHijo(nodo_id)
        
        # Índices
        for indice in self.indices:
            indice.recorrerArbol(nodo_acceso)