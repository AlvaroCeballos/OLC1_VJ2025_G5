from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato, TipoSimbolo
from .instruccion import Instruccion
from interprete.otros.enviroment import Enviroment
from interprete.otros.symbol import Symbol
from interprete.otros.errores import Error, TablaErrores
from interprete.otros.reporteVectores import ReporteVectores
from interprete.otros.tabla_procedimientos import TablaProcedimientos

class IRunProce(Instruccion):
    def __init__(self,id,argumentos, linea, columna):
        self.id = id
        self.argumentos = argumentos #lista de argumentos
        self.linea = linea
        self.columna = columna

    def ejecutar(self, env : Enviroment):
        proc = TablaProcedimientos.obtener(self.id)
        entorno_local = Enviroment(env, self.id)
        if not proc:
            err = Error(
                tipo='Semántico',
                linea=self.linea,
                columna=self.columna,
                descripcion=f'El procedimiento {self.id} no existe.'
            )
            TablaErrores.addError(err)
            return
        
        
        #validamos que los argumentos sean del mismo tipo que los parametros
        
        if len(proc.parametros) != len(self.argumentos):
            err = Error(
                tipo='Semántico',
                linea=self.linea,
                columna=self.columna,
                descripcion=f'Cantidad de parámetros incorrecta en la llamada a {self.id}.'
            )
            TablaErrores.addError(err)
            return

        # Validar tipos y que no sean expresiones complejas
        valores_param = []
        for (tipo_decl, nombre), arg in zip(proc.parametros, self.argumentos):
            # Solo se permiten literales o IDs (no expresiones ni llamadas)
            if hasattr(arg, 'es_expresion_compleja') and arg.es_expresion_compleja:
                err = Error(
                    tipo='Semántico',
                    linea=self.linea,
                    columna=self.columna,
                    descripcion=f'No se permiten expresiones complejas como parámetro en EXEC.'
                )
                TablaErrores.addError(err)
                return
            # Aquí deberías evaluar el argumento si es un ID o literal
            valor = arg.ejecutar(env) if hasattr(arg, 'ejecutar') else arg
            # Validar tipo
            if hasattr(valor, 'tipo') and valor.tipo != tipo_decl:
                err = Error(
                    tipo='Semántico',
                    linea=self.linea,
                    columna=self.columna,
                    descripcion=f'Tipo de parámetro incorrecto en la llamada a {self.id}.'
                )
                TablaErrores.addError(err)
                return
            valores_param.append(valor)

        print(f"Ejecutando procedimiento {self.id} con argumentos {[getattr(arg, 'valor', arg) for arg in self.argumentos]}")
       # Crear entorno local para el procedimiento
        

        # Declarar parámetros como variables locales
        for (tipo, nombre), valor in zip(proc.parametros, valores_param):
            # Si valor es un Retorno, extrae el tipo y el valor primitivo
            if hasattr(valor, 'valor') and hasattr(valor, 'tipo'):
                simbolo = Symbol(TipoSimbolo.VARIABLE, valor.tipo, nombre, valor.valor, entorno_local.ambito)
            else:
                simbolo = Symbol(TipoSimbolo.VARIABLE, tipo, nombre, valor, entorno_local.ambito)
            entorno_local.insertar_simbolo(nombre, simbolo)
            print(f"DEBUG: Declarado parámetro {nombre}={getattr(valor, 'valor', valor)} en entorno {entorno_local.ambito}")
        # Ejecutar instrucciones del procedimiento en el entorno local
        for instruccion in proc.instrucciones:
            instruccion.ejecutar(entorno_local)

    def recorrerArbol(self, raiz):
        
        id_nodo = AST.generarId()
        nodo_exec = Nodo(id=id_nodo, valor=f"EXEC {self.id}", hijos=[])
        raiz.addHijo(nodo_exec)
        # Argumentos
        if self.argumentos:
            id_args = AST.generarId()
            nodo_args = Nodo(id=id_args, valor="Argumentos", hijos=[])
            for arg in self.argumentos:
                if hasattr(arg, "recorrerArbol"):
                    arg.recorrerArbol(nodo_args)
                else:
                    nodo_args.addHijo(Nodo(id=AST.generarId(), valor=str(arg), hijos=[]))
            nodo_exec.addHijo(nodo_args)
        