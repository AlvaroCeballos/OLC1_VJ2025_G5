from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato, TipoSimbolo
from .instruccion import Instruccion
from interprete.otros.enviroment import Enviroment
from interprete.otros.symbol import Symbol
from interprete.otros.errores import Error, TablaErrores
from interprete.otros.reporteVectores import ReporteVectores
from interprete.otros.symbolVector import SymbolVector

class Vector(Instruccion):
    def __init__(self, text_val: str, id: str, tipo_dato: TipoDato, dimensiones: list, 
                 valores_iniciales=None, linea: int = 0, columna: int = 0):
        super().__init__(text_val, linea, columna)
        self.id = id
        self.tipo_dato = tipo_dato
        self.dimensiones = dimensiones  # Lista de enteros [2, 3] para matrix 2x3
        self.valores_iniciales = valores_iniciales  # Lista de listas [[1,2,3], [4,5,6]]
        
    def ejecutar(self, env: Enviroment):
        # Validar que las dimensiones sean números enteros positivos
        for i, dim in enumerate(self.dimensiones):
            resultado_dim = dim.ejecutar(env)
            if resultado_dim.tipo != TipoDato.INT:
                err = Error(
                    tipo='Semántico',
                    linea=self.linea,
                    columna=self.columna,
                    descripcion=f'La dimensión {i+1} del vector debe ser un número entero'
                )
                TablaErrores.addError(err)
                return self
            
            if resultado_dim.valor <= 0:
                err = Error(
                    tipo='Semántico',
                    linea=self.linea,
                    columna=self.columna,
                    descripcion=f'La dimensión {i+1} del vector debe ser mayor a 0'
                )
                TablaErrores.addError(err)
                return self
        
        # Calcular tamaño total del vector (multiplicar todas las dimensiones)
        tamanio_total = 1
        dimensiones_evaluadas = []
        for dim in self.dimensiones:
            dim_val = dim.ejecutar(env).valor
            dimensiones_evaluadas.append(dim_val)
            tamanio_total *= dim_val
            
        # Inicializar vector lineal con valores por defecto
        vector_lineal = self._inicializar_vector_defecto(tamanio_total)
        
        # Si hay valores iniciales, procesarlos
        if self.valores_iniciales:
            vector_lineal = self._procesar_valores_iniciales(env, dimensiones_evaluadas, tamanio_total)
            if vector_lineal is None:  # Error en procesamiento
                return self
        
        # Crear el símbolo del vector
        simbolo_vector = SymbolVector(
            tipo_simbolo=TipoSimbolo.VECTOR,
            tipo=self.tipo_dato,
            id=self.id,
            dimensiones=dimensiones_evaluadas,
            datos=vector_lineal,
            tamanio_total=tamanio_total,
            ambito=env.ambito
        )
        
        # INSERTAR EN TABLA DE VECTORES
        env.insertar_vector(self.id, simbolo_vector)

        # SOLO REPORTAR EL VECTOR - NO AGREGAR A TABLA DE SÍMBOLOS
        ReporteVectores.addVector(
            id_vector=self.id,
            tipo=self.tipo_dato.name,
            dimensiones=dimensiones_evaluadas,
            datos_lineales=vector_lineal,
            tamanio_total=tamanio_total,
            ambito=env.ambito
        )
        
        return self
    
    def _inicializar_vector_defecto(self, tamanio):
        """Inicializa vector con valores por defecto según el tipo"""
        if self.tipo_dato == TipoDato.INT:
            return [0] * tamanio
        elif self.tipo_dato == TipoDato.FLOAT:
            return [0.0] * tamanio
        elif self.tipo_dato == TipoDato.BOOL:
            return [False] * tamanio
        elif self.tipo_dato == TipoDato.CHAR:
            return ['\0'] * tamanio
        elif self.tipo_dato == TipoDato.STR:
            return [''] * tamanio
        else:
            return [None] * tamanio
    
    def _procesar_valores_iniciales(self, env, dimensiones, tamanio_total):
        """Procesa los valores iniciales y los convierte a representación lineal"""
        try:
            # Aplanar los valores iniciales a una lista lineal
            valores_planos = []
            self._aplanar_valores(self.valores_iniciales, valores_planos, env)
            
            # Verificar que la cantidad de valores coincida
            if len(valores_planos) != tamanio_total:
                err = Error(
                    tipo='Semántico',
                    linea=self.linea,
                    columna=self.columna,
                    descripcion=f'Se esperaban {tamanio_total} valores, pero se proporcionaron {len(valores_planos)}'
                )
                TablaErrores.addError(err)
                return None
            
            # Verificar tipos
            vector_final = []
            for i, valor_expr in enumerate(valores_planos):
                resultado = valor_expr.ejecutar(env)
                
                # Validar tipo
                if not self._tipos_compatibles(resultado.tipo, self.tipo_dato):
                    err = Error(
                        tipo='Semántico',
                        linea=self.linea,
                        columna=self.columna,
                        descripcion=f'El valor en posición {i} es de tipo {resultado.tipo.name}, se esperaba {self.tipo_dato.name}'
                    )
                    TablaErrores.addError(err)
                    return None
                
                vector_final.append(resultado.valor)
            
            return vector_final
            
        except Exception as e:
            err = Error(
                tipo='Semántico',
                linea=self.linea,
                columna=self.columna,
                descripcion=f'Error al procesar valores iniciales: {str(e)}'
            )
            TablaErrores.addError(err)
            return None
    
    def _aplanar_valores(self, valores, resultado, env):
        """Convierte estructura anidada de valores a lista plana"""
        for valor in valores:
            if isinstance(valor, list):
                self._aplanar_valores(valor, resultado, env)
            else:
                resultado.append(valor)
    
    def _tipos_compatibles(self, tipo1, tipo2):
        """Verifica si dos tipos son compatibles"""
        if tipo1 == tipo2:
            return True
        # Permitir conversión de int a float
        if tipo1 == TipoDato.INT and tipo2 == TipoDato.FLOAT:
            return True
        return False
    
    def recorrerArbol(self, raiz: Nodo):
        id_vector = AST.generarId()
        nodo_vector = Nodo(id=id_vector, valor='VECTOR', hijos=[])
        raiz.addHijo(nodo_vector)
        
        # Nodo del tipo
        id_tipo = AST.generarId()
        nodo_tipo = Nodo(id=id_tipo, valor=self.tipo_dato.name, hijos=[])
        nodo_vector.addHijo(nodo_tipo)
        
        # Nodo del ID
        id_id = AST.generarId()
        nodo_id = Nodo(id=id_id, valor=self.id, hijos=[])
        nodo_vector.addHijo(nodo_id)
        
        # Nodo de dimensiones
        id_dims = AST.generarId()
        nodo_dims = Nodo(id=id_dims, valor='DIMENSIONES', hijos=[])
        nodo_vector.addHijo(nodo_dims)
        
        for dim in self.dimensiones:
            dim.recorrerArbol(nodo_dims)
        
        # Nodo de valores iniciales (si existen)
        if self.valores_iniciales:
            id_vals = AST.generarId()
            nodo_vals = Nodo(id=id_vals, valor='VALORES', hijos=[])
            nodo_vector.addHijo(nodo_vals)