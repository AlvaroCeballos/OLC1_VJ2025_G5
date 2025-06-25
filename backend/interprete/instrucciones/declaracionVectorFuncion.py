from interprete.otros.ast import *
from .instruccion import Instruccion
from interprete.otros.tipos import TipoDato, TipoSimbolo
from interprete.otros.errores import Error, TablaErrores
from interprete.otros.symbol import Symbol

class DeclaracionVectorFuncion(Instruccion):
    def __init__(self, text_val, id_vector, tipo_dato, dimensiones, funcion_vector, linea, columna):
        super().__init__(text_val, linea, columna)
        self.id_vector = id_vector
        self.tipo_dato = tipo_dato
        self.dimensiones = dimensiones
        self.funcion_vector = funcion_vector

    def ejecutar(self, env):
        # Primero validar dimensiones
        dimensiones_evaluadas = []
        tamanio_total = 1
        
        for i, dim in enumerate(self.dimensiones):
            resultado_dim = dim.ejecutar(env)
            if resultado_dim.tipo != TipoDato.INT:
                TablaErrores.addError(Error(
                    tipo='Semántico',
                    linea=self.linea, columna=self.columna,
                    descripcion=f'La dimensión {i+1} del vector debe ser un número entero'
                ))
                return self
            
            if resultado_dim.valor <= 0:
                TablaErrores.addError(Error(
                    tipo='Semántico',
                    linea=self.linea, columna=self.columna,
                    descripcion=f'La dimensión {i+1} del vector debe ser mayor a 0'
                ))
                return self
            
            dimensiones_evaluadas.append(resultado_dim.valor)
            tamanio_total *= resultado_dim.valor
        
        # Ejecutar la función (sort o shuffle)
        resultado_funcion = self.funcion_vector.ejecutar(env)
        
        if resultado_funcion.tipo == TipoDato.ERROR:
            return self
        
        # Verificar que el tamaño coincida
        if resultado_funcion.valor['tamanio_total'] != tamanio_total:
            TablaErrores.addError(Error(
                tipo='Semántico',
                linea=self.linea, columna=self.columna,
                descripcion='El vector destino debe tener el mismo tamaño que el vector del parámetro'
            ))
            return self
        
        # Crear el símbolo del nuevo vector
        simbolo = Symbol(
            tipo_simbolo=TipoSimbolo.VECTOR,
            tipo=self.tipo_dato,
            id=self.id_vector,
            valor={
                'dimensiones': dimensiones_evaluadas,
                'datos': resultado_funcion.valor['datos'],
                'tamanio_total': tamanio_total
            },
            ambito=env.ambito,
            parametros=[],
            instrucciones=[],
            direccion=''
        )
        
        env.insertar_simbolo(self.id_vector, simbolo)
        
        return self