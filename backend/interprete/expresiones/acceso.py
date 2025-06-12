from interprete.otros.ast import *
from interprete.otros.symbol import Symbol
from interprete.otros.enviroment import Enviroment
from interprete.otros.tipos import TipoDato
from .expresion import Expresion
from interprete.otros.retorno import Retorno
from interprete.otros.tipos import TipoSimbolo
from interprete.otros.errores import Error, TablaErrores

class Acceso(Expresion):
    def __init__(self, text_val:str, id:str, linea:int, columna:int):
        super().__init__(text_val, linea, columna)
        self.id = id
        self.linea = linea
        self.columna = columna
    
    def ejecutar(self, env:Enviroment):
        resultado = Retorno(tipo=TipoDato.ERROR, valor=None)

        # Si no existe la variable en alguna tabla de simbolos
        if not env.existe_simbolo(self.id, TipoSimbolo.VARIABLE):
            # Agregando a la tabla de erorres
            #Verifica si la variable esta repetida en el archivo de entrada
            err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'No existe una variable con el nombre {self.id}')
            TablaErrores.addError(err)
            return resultado
                
        simbolo:Symbol = env.getSimbolo(self.id, TipoSimbolo.VARIABLE)

        resultado = Retorno(tipo=simbolo.tipo, valor=simbolo.valor)
        
        return resultado
        
    def recorrerArbol(self, raiz:Nodo):
        id = AST.generarId()
        hijo = Nodo(id=id, valor=self.id, hijos=[])
        raiz.addHijo(hijo)