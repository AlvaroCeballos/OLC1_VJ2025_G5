from interprete.otros.ast import *
from operator import truediv
from interprete.otros.retorno import Retorno
from interprete.otros.tipos import TipoDato, TipoSimbolo
from interprete.instrucciones.instruccion import Instruccion
from interprete.expresiones.expresion import Expresion
from interprete.otros.enviroment import Enviroment
from interprete.otros.errores import Error, TablaErrores
from interprete.expresiones.tipoChars import TipoChars

class Asignacion(Instruccion):
    def __init__(self, text_val:str, id:str, expresion:Expresion, linea:int, columna:int):
        super().__init__(text_val, linea, columna)
        self.id = id
        self.expresion = expresion
        self.linea = linea
        self.columna = columna
    
    def ejecutar(self, env:Enviroment):
        # Validar que la variable exista en la tabla de simbolos
        if not env.existe_simbolo(self.id, TipoSimbolo.VARIABLE):
            # Agregando a la tabla de erorres
            err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error de asignacion de variable. No existe una variable con el nombre {self.id}')
            TablaErrores.addError(err)
            return self

        simbolo = env.getSimbolo(self.id, TipoSimbolo.VARIABLE)
        exp = self.expresion.ejecutar(env)

        if exp.tipo == TipoDato.ERROR:
            # Agregando error a la tabla de erorres
            err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion='Error en la asignacion de variable')
            TablaErrores.addError(err)
            return self
        
        if simbolo.tipo == TipoDato.INT:
            if exp.tipo != TipoDato.INT:
                # Agregando error a la tabla de erorres
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error de asignacion de variable. No se puede asignar un valor de tipo {exp.tipo.name} a una variable de tipo {simbolo.tipo.name}')
                TablaErrores.addError(err)
                return self
            valor_int = int(exp.valor)
            if not (-2147483648 <= valor_int <= 2147483647):
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'El valor {exp.valor} está fuera del rango permitido para INT')
                TablaErrores.addError(err)
                return self       
            simbolo.valor = valor_int
        elif simbolo.tipo == TipoDato.FLOAT:
            if exp.tipo not in [TipoDato.FLOAT, TipoDato.INT]:
                # Agregando error a la tabla de erorres
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error de asignacion de variable. No se puede asignar un valor de tipo {exp.tipo.name} a una variable de tipo {simbolo.tipo.name}')
                TablaErrores.addError(err)
                return self
            simbolo.valor = float(exp.valor)
        elif simbolo.tipo == TipoDato.STR:
            if exp.tipo != TipoDato.STR:
                # Agregando error a la tabla de erorres
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error de asignacion de variable. No se puede asignar un valor de tipo {exp.tipo.name} a una variable de tipo {simbolo.tipo.name}')
                TablaErrores.addError(err)
                return self
            simbolo.valor = str(exp.valor)
        elif simbolo.tipo == TipoDato.CHAR:
            if exp.tipo != TipoDato.CHAR:
                # Agregando error a la tabla de erorres
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error de asignacion de variable. No se puede asignar un valor de tipo {exp.tipo.name} a una variable de tipo {simbolo.tipo.name}')
                TablaErrores.addError(err)
                return self
            simbolo.valor = str(exp.valor)
        elif simbolo.tipo == TipoDato.BOOLEAN:
            if exp.tipo != TipoDato.BOOLEAN:
                # Agregando error a la tabla de erorres
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error de asignacion de variable. No se puede asignar un valor de tipo {exp.tipo.name} a una variable de tipo {simbolo.tipo.name}')
                TablaErrores.addError(err)
                return self
            simbolo.valor = bool(exp.valor)
        elif simbolo.tipo == TipoDato.UNDEFINED:
            if exp.tipo not in [TipoDato.INT, TipoDato.FLOAT, TipoDato.STR, TipoDato.CHAR, TipoDato.BOOLEAN]:
                # Agregando error a la tabla de erorres
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error de asignacion de variable. No se puede asignar un valor de tipo {exp.tipo.name} a una variable de tipo {simbolo.tipo.name}')
                TablaErrores.addError(err)
                return self
            simbolo.valor = exp.valor
        elif simbolo.tipo == TipoDato.NULL:
            if exp.tipo not in [TipoDato.INT, TipoDato.FLOAT, TipoDato.STR, TipoDato.CHAR, TipoDato.BOOLEAN]:
                # Agregando error a la tabla de erorres
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error de asignacion de variable. No se puede asignar un valor de tipo {exp.tipo.name} a una variable de tipo {simbolo.tipo.name}')
                TablaErrores.addError(err)
                return self
            simbolo.valor = exp.valor
        else:
            # Agregando error a la tabla de erorres
            err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error de asignacion de variable. No se puede asignar un valor de tipo {exp.tipo.name} a una variable de tipo {simbolo.tipo.name}')
            TablaErrores.addError(err)
            return self

    def recorrerArbol(self, raiz:Nodo):
        id = AST.generarId()
        hijo = Nodo(id=id, valor='ASIGNACION', hijos=[])
        raiz.addHijo(hijo)
        id = AST.generarId()
        hijo.addHijo(Nodo(id=id, valor=self.id, hijos=[]))
        self.expresion.recorrerArbol(hijo)
        