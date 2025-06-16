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
        # Simbolo a insertar en tabla de simbolos
        print('Insertado en TS: ', self.id)
        retorno = self.valor.ejecutar(env) if isinstance(self.valor, Expresion) else self.valor
        simbolo = Symbol(TipoSimbolo.VARIABLE, retorno.tipo, self.id, retorno.valor, env.ambito, None)

        # Guardando con un valor por defecto
        if self.valor is None:
            if self.tipo == TipoDato.INT:
                simbolo.valor = 0
            elif self.tipo == TipoDato.FLOAT:
                simbolo.valor = 0.0
            elif self.tipo == TipoDato.STR:
                simbolo.valor = ' '
            elif self.tipo == TipoDato.CHAR:
                simbolo.valor = ' '
            elif self.tipo == TipoDato.BOOLEAN:
                simbolo.valor = True

        # Siempre insertar/sobrescribir (sin verificar existencia)
        env.insertar_simbolo(self.id, simbolo)
        
        if env.existe_simbolo_ent_actual(self.id, TipoSimbolo.VARIABLE):
            print(f'Variable {self.id} redeclarada, sobrescribiendo')
        else:
            print(f'Variable {self.id} declarada por primera vez')

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
            hijo.addHijo(Nodo(id=id, valor=self.valor, hijos=[]))
        else:
            id = AST.generarId()
            hijo.addHijo(Nodo(id=id, valor='None', hijos=[]))
        

