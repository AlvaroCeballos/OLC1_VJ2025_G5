from interprete.otros.ast import *
import random
from interprete.otros.enviroment import Enviroment
from interprete.expresiones.expresion import Expresion
from interprete.otros.tipos import TipoDato, TipoSimbolo
from interprete.otros.retorno import Retorno
from interprete.otros.errores import TablaErrores, Error

class Sort(Expresion):
    def __init__(self, text_val: str, vector_arg, linea: int, columna: int):
        super().__init__(text_val, linea, columna)
        self.vector_arg = vector_arg  # ID del vector o expresión que devuelve vector

    def ejecutar(self, env: Enviroment):
        # Si es un ID, buscar el vector
        if hasattr(self.vector_arg, 'id'):  # Es un Acceso
            vector_id = self.vector_arg.id
            simbolo = env.getSimbolo(vector_id, TipoSimbolo.VECTOR)
            
            if simbolo is None:
                TablaErrores.addError(Error(
                    tipo='Semántico',
                    linea=self.linea, columna=self.columna,
                    descripcion=f'No existe un vector con el nombre {vector_id}'
                ))
                return Retorno(TipoDato.ERROR, None)
            
            if simbolo.tipo_simbolo != TipoSimbolo.VECTOR:
                TablaErrores.addError(Error(
                    tipo='Semántico',
                    linea=self.linea, columna=self.columna,
                    descripcion=f'{vector_id} no es un vector'
                ))
                return Retorno(TipoDato.ERROR, None)
            
            # Verificar que sea un vector numérico de una dimensión
            dimensiones = simbolo.valor['dimensiones']
            if len(dimensiones) != 1:
                TablaErrores.addError(Error(
                    tipo='Semántico',
                    linea=self.linea, columna=self.columna,
                    descripcion='sort() solo acepta vectores de una dimensión'
                ))
                return Retorno(TipoDato.ERROR, None)
            
            if simbolo.tipo not in (TipoDato.INT, TipoDato.FLOAT):
                TablaErrores.addError(Error(
                    tipo='Semántico',
                    linea=self.linea, columna=self.columna,
                    descripcion='sort() solo acepta vectores numéricos (int o float)'
                ))
                return Retorno(TipoDato.ERROR, None)
            
            # Crear una copia del vector y ordenarla
            datos_originales = simbolo.valor['datos'].copy()
            datos_ordenados = sorted(datos_originales)
            
            # Crear un nuevo vector con los datos ordenados
            nuevo_vector = {
                'dimensiones': dimensiones.copy(),
                'datos': datos_ordenados,
                'tamanio_total': simbolo.valor['tamanio_total']
            }
            
            return Retorno(simbolo.tipo, nuevo_vector)
        
        else:
            TablaErrores.addError(Error(
                tipo='Semántico',
                linea=self.linea, columna=self.columna,
                descripcion='sort() requiere un vector como parámetro'
            ))
            return Retorno(TipoDato.ERROR, None)
    
    def recorrerArbol(self, raiz: Nodo):
        id_sort = AST.generarId()
        nodo = Nodo(id_sort, 'SORT', hijos=[])
        raiz.hijos.append(nodo)
        self.vector_arg.recorrerArbol(nodo)

class Shuffle(Expresion):
    def __init__(self, text_val: str, vector_arg, linea: int, columna: int):
        super().__init__(text_val, linea, columna)
        self.vector_arg = vector_arg

    def ejecutar(self, env: Enviroment):
        # Si es un ID, buscar el vector
        if hasattr(self.vector_arg, 'id'):  # Es un Acceso
            vector_id = self.vector_arg.id
            simbolo = env.getSimbolo(vector_id, TipoSimbolo.VECTOR)
            
            if simbolo is None:
                TablaErrores.addError(Error(
                    tipo='Semántico',
                    linea=self.linea, columna=self.columna,
                    descripcion=f'No existe un vector con el nombre {vector_id}'
                ))
                return Retorno(TipoDato.ERROR, None)
            
            if simbolo.tipo_simbolo != TipoSimbolo.VECTOR:
                TablaErrores.addError(Error(
                    tipo='Semántico',
                    linea=self.linea, columna=self.columna,
                    descripcion=f'{vector_id} no es un vector'
                ))
                return Retorno(TipoDato.ERROR, None)
            
            # Verificar que el vector de destino tenga el mismo tamaño
            dimensiones = simbolo.valor['dimensiones']
            
            # Crear una copia del vector y mezclarla
            datos_originales = simbolo.valor['datos'].copy()
            
            # Si es multidimensional, reorganizar por columna mayor
            if len(dimensiones) == 2:
                filas, columnas = dimensiones
                # Convertir de row-major a column-major y mezclar
                datos_column_major = []
                for col in range(columnas):
                    for fila in range(filas):
                        idx = fila * columnas + col
                        datos_column_major.append(datos_originales[idx])
                random.shuffle(datos_column_major)
                datos_mezclados = datos_column_major
            else:
                # Para vectores de una dimensión, mezclar directamente
                datos_mezclados = datos_originales.copy()
                random.shuffle(datos_mezclados)
            
            # Crear un nuevo vector con los datos mezclados
            nuevo_vector = {
                'dimensiones': dimensiones.copy(),
                'datos': datos_mezclados,
                'tamanio_total': simbolo.valor['tamanio_total']
            }
            
            return Retorno(simbolo.tipo, nuevo_vector)
        
        else:
            TablaErrores.addError(Error(
                tipo='Semántico',
                linea=self.linea, columna=self.columna,
                descripcion='shuffle() requiere un vector como parámetro'
            ))
            return Retorno(TipoDato.ERROR, None)
    
    def recorrerArbol(self, raiz: Nodo):
        id_shuffle = AST.generarId()
        nodo = Nodo(id_shuffle, 'SHUFFLE', hijos=[])
        raiz.hijos.append(nodo)
        self.vector_arg.recorrerArbol(nodo)