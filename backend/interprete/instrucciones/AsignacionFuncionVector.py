from interprete.otros.ast import *
from .instruccion import Instruccion
from interprete.otros.tipos import TipoDato, TipoSimbolo
from interprete.otros.errores import Error, TablaErrores
from interprete.otros.symbol import Symbol

class AsignacionFuncionVector(Instruccion):
    def __init__(self, text_val, id_destino, funcion_vector, linea, columna):
        super().__init__(text_val, linea, columna)
        self.id_destino = id_destino
        self.funcion_vector = funcion_vector  # Sort o Shuffle

    def ejecutar(self, env):
        # Ejecutar la función (sort o shuffle)
        resultado = self.funcion_vector.ejecutar(env)
        
        if resultado.tipo == TipoDato.ERROR:
            return self
        
        # Buscar el vector destino
        simbolo_destino = env.getSimbolo(self.id_destino, TipoSimbolo.VECTOR)
        
        if simbolo_destino is None:
            TablaErrores.addError(Error('Semántico', self.linea, self.columna, 
                                      f'No existe un vector con el nombre {self.id_destino}'))
            return self
        
        if simbolo_destino.tipo_simbolo != TipoSimbolo.VECTOR:
            TablaErrores.addError(Error('Semántico', self.linea, self.columna, 
                                      f'{self.id_destino} no es un vector'))
            return self
        
        # Verificar que los vectores tengan el mismo tamaño
        if (simbolo_destino.valor['tamanio_total'] != resultado.valor['tamanio_total'] or
            simbolo_destino.valor['dimensiones'] != resultado.valor['dimensiones']):
            TablaErrores.addError(Error('Semántico', self.linea, self.columna, 
                                      'El vector destino debe tener el mismo tamaño que el vector del parámetro'))
            return self
        
        # Verificar compatibilidad de tipos
        if simbolo_destino.tipo != resultado.tipo:
            TablaErrores.addError(Error('Semántico', self.linea, self.columna, 
                                      'Los vectores deben ser del mismo tipo'))
            return self
        
        # Actualizar los datos del vector destino
        simbolo_destino.valor['datos'] = resultado.valor['datos']
        
        return self