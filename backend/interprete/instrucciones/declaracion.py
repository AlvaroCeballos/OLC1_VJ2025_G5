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
        # Evaluar la expresión si existe
        if self.valor is not None and isinstance(self.valor, Expresion):
            retorno = self.valor.ejecutar(env)
            tipo = retorno.tipo
            valor_final = retorno.valor
            expresion_original = self.valor  # Guardar la expresión original
        else:
            # Valor por defecto según el tipo
            tipo = self.tipo
            if self.tipo == TipoDato.INT:
                valor_final = 0
            elif self.tipo == TipoDato.FLOAT:
                valor_final = 0.0
            elif self.tipo == TipoDato.STR:
                valor_final = ' '
            elif self.tipo == TipoDato.CHAR:
                valor_final = ' '
            elif self.tipo == TipoDato.BOOL:
                valor_final = True
            else:
                valor_final = None
            expresion_original = None

        # Crear símbolo (esto permite sobreescribir si ya existe)
        simbolo = Symbol(TipoSimbolo.VARIABLE, tipo, self.id, valor_final, env.ambito, None)
        env.insertar_simbolo(self.id, simbolo)

        # Si había una expresión inicial, hacer la asignación CORRECTAMENTE
        if expresion_original is not None:
            from interprete.instrucciones.asignacion import Asignacion
            asignacion = Asignacion(self.text_val, self.id, expresion_original, self.linea, self.columna)
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