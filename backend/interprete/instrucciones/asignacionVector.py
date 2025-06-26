# archivo: backend/interprete/instrucciones/asignacionVector.py
from interprete.otros.ast import *
from .instruccion import Instruccion
from interprete.otros.tipos import TipoDato, TipoSimbolo
from interprete.otros.errores import Error, TablaErrores

class AsignacionVector(Instruccion):
    def __init__(self, text_val, id_vector, indices, expresion, linea, columna):
        super().__init__(text_val, linea, columna)
        self.id_vector = id_vector
        self.indices = indices  # Lista de expresiones para los índices
        self.expresion = expresion  # Expresión del valor a asignar
    
    def ejecutar(self, env):
        # Buscar el vector
        simbolo = env.getSimbolo(self.id_vector, TipoSimbolo.VECTOR)
        if simbolo is None:
            TablaErrores.addError(Error('Semántico', self.linea, self.columna, 
                                      f'No existe un vector con el nombre {self.id_vector}'))
            return self
        
        # Evaluar los índices
        indices_evaluados = []
        for idx_expr in self.indices:
            resultado = idx_expr.ejecutar(env)
            if resultado.tipo != TipoDato.INT:
                TablaErrores.addError(Error('Semántico', self.linea, self.columna, 
                                          'Los índices del vector deben ser enteros'))
                return self
            indices_evaluados.append(resultado.valor)
        
        # Evaluar la expresión del valor
        resultado_valor = self.expresion.ejecutar(env)
        if resultado_valor.tipo == TipoDato.ERROR:
            return self
        
        # Validar tipo
        if not self._tipos_compatibles(resultado_valor.tipo, simbolo.tipo):
            TablaErrores.addError(Error('Semántico', self.linea, self.columna, 
                                      f'No se puede asignar un valor de tipo {resultado_valor.tipo.name} a un vector de tipo {simbolo.tipo.name}'))
            return self
        
        # Validar dimensiones y rangos (similar a AccesoVector)
        dimensiones = simbolo.valor['dimensiones']
        if len(indices_evaluados) != len(dimensiones):
            TablaErrores.addError(Error('Semántico', self.linea, self.columna, 
                                      f'El vector tiene {len(dimensiones)} dimensiones, pero se proporcionaron {len(indices_evaluados)} índices'))
            return self
        
        for i, (indice, dimension) in enumerate(zip(indices_evaluados, dimensiones)):
            if indice < 0 or indice >= dimension:
                TablaErrores.addError(Error('Semántico', self.linea, self.columna, 
                                          f'Índice {indice} fuera de rango para la dimensión {i+1} (0-{dimension-1})'))
                return self
        
        # Calcular posición y asignar
        posicion_lineal = self._calcular_posicion_lineal(indices_evaluados, dimensiones)
        simbolo.valor['datos'][posicion_lineal] = resultado_valor.valor
        
        return self
    
    def _calcular_posicion_lineal(self, indices, dimensiones):
        """Igual que en AccesoVector"""
        posicion = 0
        multiplicador = 1
        for i in range(len(indices) - 1, -1, -1):
            posicion += indices[i] * multiplicador
            if i > 0:
                multiplicador *= dimensiones[i]
        return posicion
    
    def _tipos_compatibles(self, tipo1, tipo2):
        if tipo1 == tipo2:
            return True
        if tipo1 == TipoDato.INT and tipo2 == TipoDato.FLOAT:
            return True
        return False