from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato
from interprete.otros.retorno import Retorno
from interprete.otros.enviroment import Enviroment
from interprete.otros.errores import Error, TablaErrores
from .expresion import Expresion

class Logica(Expresion):
    def __init__(self, izquierda, derecha, operador, linea, columna):
        super().__init__('', linea, columna)
        self.izquierda = izquierda
        self.derecha = derecha
        self.operador = operador
        self.text_val = f'{operador}({getattr(izquierda, "text_val", izquierda)},{getattr(derecha, "text_val", derecha)})'

    def ejecutar(self, env: Enviroment):
        if self.operador == '!':
            der = self.derecha.ejecutar(env)
            if der.tipo != TipoDato.BOOL:
                TablaErrores.addError(Error('Semántico', self.linea, self.columna, 'NOT solo acepta booleanos'))
                return Retorno(tipo=TipoDato.ERROR, valor=None)
            return Retorno(tipo=TipoDato.BOOL, valor=not der.valor)
        else:
            izq = self.izquierda.ejecutar(env)
            der = self.derecha.ejecutar(env)
            if izq.tipo != TipoDato.BOOL or der.tipo != TipoDato.BOOL:
                TablaErrores.addError(Error('Semántico', self.linea, self.columna, f'{self.operador.upper()} solo acepta booleanos'))
                return Retorno(tipo=TipoDato.ERROR, valor=None)
            if self.operador == '&&':
                return Retorno(tipo=TipoDato.BOOL, valor=izq.valor and der.valor)
            elif self.operador == '||':
                return Retorno(tipo=TipoDato.BOOL, valor=izq.valor or der.valor)
            elif self.operador == '^':
                return Retorno(tipo=TipoDato.BOOL, valor=izq.valor != der.valor)
        return Retorno(tipo=TipoDato.ERROR, valor=None)
    
    def recorrerArbol(self, raiz: Nodo):
        id = AST.generarId()  # O Nodo.generarId() si lo agregas ahí
        raiz.id = id
        raiz.valor = self.operador.upper()
        if self.izquierda is not None:
            hijo_izq = Nodo()
            self.izquierda.recorrerArbol(hijo_izq)
            raiz.hijos.append(hijo_izq)
        hijo_der = Nodo()
        self.derecha.recorrerArbol(hijo_der)
        raiz.hijos.append(hijo_der)