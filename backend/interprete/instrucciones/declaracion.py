from interprete.otros.ast import *
from interprete.expresiones.tipoChars import TipoChars
from interprete.otros.enviroment import Enviroment
from interprete.otros.tipos import TipoSimbolo
from interprete.instrucciones.instruccion import Instruccion
from interprete.expresiones.expresion import Expresion
from interprete.otros.tipos import TipoDato
from interprete.otros.retorno import Retorno
from interprete.otros.symbol import Symbol
from interprete.otros.errores import Error, TablaErrores
from interprete.expresiones.literal import Literal
from interprete.instrucciones.asignacion import Asignacion

class Declaracion(Instruccion):
    def __init__(self, text_val:str, id:str, tipo:TipoDato, valor:str, linea:int, columna:int):
        super().__init__(text_val, linea, columna)
        self.id = id
        self.valor = valor

        if isinstance(tipo, TipoChars): 
            self.tipo = tipo.charTipo
        else:
            self.tipo = tipo
        
    def ejecutar(self, env:Enviroment):
        #print('Insertado en TS: ', self.id)
        if self.valor is not None and isinstance(self.valor, Expresion):
            retorno = self.valor.ejecutar(env)
            tipo = retorno.tipo
            valor = retorno.valor
        else:
            # Valor por defecto según el tipo
            tipo = self.tipo
            if self.tipo == TipoDato.INT:
                valor = 0
            elif self.tipo == TipoDato.FLOAT:
                valor = 0.0
            elif self.tipo == TipoDato.STR:
                valor = ' '
            elif self.tipo == TipoDato.CHAR:
                valor = ' '
            elif self.tipo == TipoDato.BOOL:
                valor = True
            else:
                valor = None

        simbolo = Symbol(TipoSimbolo.VARIABLE, tipo, self.id, valor, env.ambito, None)
        env.insertar_simbolo(self.id, simbolo)

        # Si hay inicialización, ejecuta la asignación
        if self.valor is not None:
            asignacion = Asignacion(self.text_val, self.id, self.valor, self.linea, self.columna)
            asignacion.ejecutar(env)

        return self
    
    def recorrerArbol(self, raiz:Nodo):
        id = AST.generarId()
        hijo = Nodo(id=id, valor='DECLARACION', hijos=[])
        raiz.addHijo(hijo)
        
        id = AST.generarId()
        hijo.addHijo(Nodo(id=id, valor=self.id, hijos=[]))
        
        id = AST.generarId()
        hijo.addHijo(Nodo(id=id, valor=self.tipo.name, hijos=[]))
        
        if self.valor is not None:
            id = AST.generarId()
            # Si es un objeto Literal, obtener su valor
            if hasattr(self.valor, 'valor'):
                hijo.addHijo(Nodo(id=id, valor=str(self.valor.valor), hijos=[]))
            else:
                hijo.addHijo(Nodo(id=id, valor=str(self.valor), hijos=[]))
        else:
            id = AST.generarId()
            hijo.addHijo(Nodo(id=id, valor='None', hijos=[]))
        

