from interprete.otros.ast import *
import math
from interprete.otros.enviroment import Enviroment
from interprete.expresiones.expresion import Expresion
from interprete.otros.tipos import TipoDato
from interprete.otros.retorno import Retorno
from interprete.otros.errores import TablaErrores, Error

class Seno(Expresion):
    def __init__(self, text_val: str, argumento, linea: int , columna: int):
        super().__init__(text_val, linea, columna)
        self.argumento = argumento

    def ejecutar(self, env: Enviroment):
        # Ejecuta el argumento y verifica el tipo de dato
        ret = self.argumento.ejecutar(env)
        if ret.tipo not in (TipoDato.INT, TipoDato.FLOAT):
            #error semantico
            from interprete.otros.errores import Error, TablaErrores
            TablaErrores.addError(Error(
                tipo='Semántico',
                linea=self.linea, columna=self.columna,
                descripcion=f'SENO sólo acepta INT o FLOAT, no {ret.tipo}'
            ))
            return Retorno(None, None)
        
        #calculamos seno siempre devolverá un float
        return Retorno(TipoDato.FLOAT, math.sin(ret.valor))
    
    def recorrerArbol(self, raiz: Nodo):
        id = AST.generarId()
        nodo = Nodo(id, 'SENO', hijos=[])
        raiz.hijos.append(nodo)
        self.argumento.recorrerArbol(nodo)

class Coseno(Expresion):
    def __init__(self, text_val: str, argumento, linea: int , columna: int):
        super().__init__(text_val, linea, columna)
        self.argumento = argumento

    def ejecutar(self, env: Enviroment):
        # Ejecuta el argumento y verifica el tipo de dato
        ret = self.argumento.ejecutar(env)
        if ret.tipo not in (TipoDato.INT, TipoDato.FLOAT):
            #error semantico
            TablaErrores.addError(Error(
                tipo='Semántico',
                linea=self.linea, columna=self.columna,
                descripcion=f'COSENO sólo acepta INT o FLOAT, no {ret.tipo}'
            ))
            return Retorno(None, None)
        
        #calculamos coseno siempre devolverá un float
        return Retorno(TipoDato.FLOAT, math.cos(ret.valor))
    
    def recorrerArbol(self, raiz: Nodo):
        id = AST.generarId()
        nodo = Nodo(id, 'COSENO', hijos=[])
        raiz.hijos.append(nodo)
        self.argumento.recorrerArbol(nodo)
                
class Inv(Expresion):
    def __init__(self, text_val: str, argumento, linea: int , columna: int):
        super().__init__(text_val, linea, columna)
        self.argumento = argumento

    def ejecutar(self, env: Enviroment):
        # Ejecuta el argumento y verifica el tipo de dato
        ret = self.argumento.ejecutar(env)
        #acepto solo errores
        if ret.tipo != TipoDato.INT:
            TablaErrores.addError(Error(
                tipo='Semántico',
                linea=self.linea, columna=self.columna,
                descripcion=f'INV sólo acepta INT, no {ret.tipo}'
            ))
            # devolvemos un Retorno de error
            return Retorno(None, TipoDato.ERROR)
        
        
        #invierte los digitos
        n = ret.valor
        s = str(abs(n))        # p.ej. "2020"
        rev_s = s[::-1]        # p.ej. "0202"
        inv = int(rev_s)       # p.ej. 202
        if n < 0:
            inv = -inv         # p.ej. -202
        return Retorno(TipoDato.INT, inv)
    
    def recorrerArbol(self, raiz: Nodo):
        id = AST.generarId()
        nodo = Nodo(id, 'INV', hijos=[])
        raiz.hijos.append(nodo)
        self.argumento.recorrerArbol(nodo)
