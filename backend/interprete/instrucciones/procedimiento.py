from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato, TipoSimbolo
from .instruccion import Instruccion
from interprete.otros.enviroment import Enviroment
from interprete.otros.symbol import Symbol
from interprete.otros.errores import Error, TablaErrores
from interprete.otros.reporteVectores import ReporteVectores
from interprete.otros.tabla_procedimientos import TablaProcedimientos

class Procedimiento(Instruccion):
    def __init__(self, text_val,id, parametros , instrucciones, linea = 0, columna = 0):
        super().__init__(text_val, linea, columna)
        self.id = id
        self.parametros = parametros #lista de parametros
        self.instrucciones = instrucciones #instrucciones que manejara el procedimiento
        self.linea = linea
        self.columna = columna

        # Validar que existan parámetros
        if not parametros or len(parametros) == 0:
            err = Error(
                tipo='Semántico',
                linea=self.linea,
                columna=self.columna,
                descripcion=f'El procedimiento {self.id} debe tener al menos un parámetro.'
            )
            TablaErrores.addError(err)
            self.valido = False
            return

        #validamos que los parametros no se repitan
        nombres = [nombre for tipo, nombre in parametros]
        if len(nombres) != len(set(nombres)):
            err = Error(
                tipo = 'semantico',
                linea = self.linea,
                columna = self.columna,
                descripcion = f'Los parametros del procedimiento {self.id} no pueden repetirse'

            )
            TablaErrores.addError(err)
            self.valido = False
            return
        
        #validamos que no vengan vectores como parametros
        for tipo, nombre in parametros:
            if hasattr(tipo, 'esVector') and tipo.es_vector:
                err = Error(
                    tipo='Semántico',
                    linea=self.linea,
                    columna=self.columna,
                    descripcion=f'No se permiten vectores como parámetros en el procedimiento {self.id}'
                )
                TablaErrores.addError(err)
                self.valido = False
                return
        
        #validamops que el nombre del procedimiento no se repita
        if TablaProcedimientos.existe(self.id):
            err = Error(
                tipo='Semántico',
                linea=self.linea,
                columna=self.columna,
                descripcion=f'El procedimiento {self.id} ya fue declarado.'
            )
            TablaErrores.addError(err)
            self.valido = False
            return
        
        
        #si todo esta bien, lo registramos
        TablaProcedimientos.agregar(self)
        self.valido = True

    def ejecutar(self, env: Enviroment):
        pass

    def recorrerArbol(self, raiz):
        id_nodo = AST.generarId()
        nodo_proc = Nodo(id=id_nodo, valor=f"PROC {self.id}", hijos=[])
        raiz.addHijo(nodo_proc)
        # Parámetros
        if self.parametros:
            id_param = AST.generarId()
            nodo_param = Nodo(id=id_param, valor="Parámetros", hijos=[])
            for tipo, nombre in self.parametros:
                nodo_param.addHijo(Nodo(id=AST.generarId(), valor=f"{tipo}:{nombre}", hijos=[]))
            nodo_proc.addHijo(nodo_param)
        # Instrucciones
        if self.instrucciones:
            id_inst = AST.generarId()
            nodo_inst = Nodo(id=id_inst, valor="Instrucciones", hijos=[])
            for inst in self.instrucciones:
                if hasattr(inst, "recorrerArbol"):
                    inst.recorrerArbol(nodo_inst)
            nodo_proc.addHijo(nodo_inst)