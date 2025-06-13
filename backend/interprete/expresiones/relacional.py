from interprete.otros.ast import *
from .expresion import Expresion
from interprete.otros.tipos import TipoRelacional, TipoDato
from interprete.otros.retorno import Retorno
from interprete.otros.enviroment import Enviroment
from interprete.otros.errores import Error, TablaErrores


class Relacional(Expresion):
    def __init__(self, izquierda, derecha, operador, linea, columna):
        super().__init__('', linea, columna)
        self.izquierda = izquierda
        self.derecha = derecha
        self.operador = operador

    def ejecutar(self, env: Enviroment):
        izq = self.izquierda.ejecutar(env)
        der = self.derecha.ejecutar(env)

        tipo_izq = izq.tipo
        tipo_der = der.tipo

        # Validación de tipos según la tabla
        valido = False
        # INT, FLOAT, CHAR entre sí
        if (tipo_izq in [TipoDato.INT, TipoDato.FLOAT, TipoDato.CHAR] and
            tipo_der in [TipoDato.INT, TipoDato.FLOAT, TipoDato.CHAR]):
            valido = True
        # STR solo con STR
        elif tipo_izq == TipoDato.STR and tipo_der == TipoDato.STR:
            valido = True
        # BOOLEAN solo con BOOLEAN
        elif tipo_izq == TipoDato.BOOLEAN and tipo_der == TipoDato.BOOLEAN:
            valido = True

        if not valido:
            err = Error(
                tipo='Semántico',
                linea=self.linea,
                columna=self.columna,
                descripcion=f'Operación relacional no válida entre {tipo_izq.name} y {tipo_der.name}'
            )
            TablaErrores.addError(err)
            return Retorno(tipo=TipoDato.ERROR, valor=None)

        resultado = False
        
        val_izq = izq.valor
        val_der = der.valor

        if tipo_izq == TipoDato.CHAR:
            val_izq = ord(val_izq)
        if tipo_der == TipoDato.CHAR:
            val_der = ord(val_der)

        if self.operador == TipoRelacional.IGUALACION:
            resultado = val_izq == val_der
        elif self.operador == TipoRelacional.DIFERENCIACION:
            resultado = val_izq != val_der
        elif self.operador == TipoRelacional.MENOR:
            resultado = val_izq < val_der
        elif self.operador == TipoRelacional.MENOR_IGUAL:
            resultado = val_izq <= val_der
        elif self.operador == TipoRelacional.MAYOR:
            resultado = val_izq > val_der
        elif self.operador == TipoRelacional.MAYOR_IGUAL:
            resultado = val_izq >= val_der
            
        else:
            err = Error(
                tipo='Semántico',
                linea=self.linea,
                columna=self.columna,
                descripcion=f'Operador relacional no reconocido'
            )
            TablaErrores.addError(err)
            return Retorno(tipo=TipoDato.ERROR, valor=None)

        return Retorno(tipo=TipoDato.BOOLEAN, valor=resultado)
    
    def recorrerArbol(self, raiz: Nodo):
        id = AST.generarId()
        nodo = Nodo(id=id, valor=self.operador, hijos=[])

        # Recorrer izquierda
        izq_id = AST.generarId()
        izq_nodo = Nodo(id=izq_id, valor='Izquierda', hijos=[])
        nodo.addHijo(izq_nodo)
        self.izquierda.recorrerArbol(izq_nodo)

        # Recorrer derecha
        der_id = AST.generarId()
        der_nodo = Nodo(id=der_id, valor='Derecha', hijos=[])
        nodo.addHijo(der_nodo)
        self.derecha.recorrerArbol(der_nodo)

        raiz.addHijo(nodo)