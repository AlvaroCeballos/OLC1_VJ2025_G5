from interprete.otros.ast import *
from .expresion import Expresion
from interprete.otros.tipos import TipoAritmetica, TipoDato
from interprete.otros.retorno import Retorno
from interprete.otros.enviroment import Enviroment
from interprete.otros.errores import Error, TablaErrores

class Aritmetica(Expresion):
    def __init__(self, text_val:str, op1:Expresion, operador:TipoAritmetica, op2:Expresion, linea, columna):
        super().__init__(text_val, linea, columna)
        self.op1 = op1
        self.op2 = op2
        self.operador = operador
    
    def ejecutar(self, env:Enviroment):
        op1:Retorno = self.op1.ejecutar(env)
        op2:Retorno = self.op2.ejecutar(env)
        resultado = Retorno(tipo=TipoDato.ERROR, valor=None)

        # Que no haya error en los operandos
        if op1.tipo == TipoDato.ERROR or op2.tipo == TipoDato.ERROR:
            # Agregando a la tabla de errores
            err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la operación aritmética.')
            TablaErrores.addError(err)
            return resultado

        if self.operador == TipoAritmetica.SUMA:
            # INT
            if op1.tipo == TipoDato.INT and op2.tipo == TipoDato.INT:
                resultado.tipo = TipoDato.INT
                resultado.valor = op1.valor + op2.valor
            
            #INT/FLOAT
            elif (op1.tipo == TipoDato.INT or op1.tipo == TipoDato.FLOAT) and (op2.tipo == TipoDato.INT or op2.tipo == TipoDato.FLOAT):
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor + op2.valor

            #INT/CHAR
            elif (op1.tipo == TipoDato.INT or op1.tipo == TipoDato.CHAR) and (op2.tipo == TipoDato.INT or op2.tipo == TipoDato.CHAR):
                resultado.tipo = TipoDato.INT
                resultado.valor = ord(op1.valor) + ord(op2.valor)
            
            #INT/STR
            elif (op1.tipo == TipoDato.INT or op1.tipo == TipoDato.STR) and (op2.tipo == TipoDato.INT or op2.tipo == TipoDato.STR):
                resultado.tipo = TipoDato.STR
                resultado.valor = str(op1.valor) + str(op2.valor)

            # FLOAT/FLOAT
            elif op1.tipo == TipoDato.FLOAT and op2.tipo == TipoDato.FLOAT:
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor + op2.valor

            # FLOAT/CHAR
            elif (op1.tipo == TipoDato.FLOAT or op1.tipo == TipoDato.CHAR) and (op2.tipo == TipoDato.FLOAT or op2.tipo == TipoDato.CHAR):
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = ord(op1.valor) + ord(op2.valor)
            
             # FLOAT/STR
            elif (op1.tipo == TipoDato.FLOAT or op1.tipo == TipoDato.STR) and (op2.tipo == TipoDato.FLOAT or op2.tipo == TipoDato.STR):
                resultado.tipo = TipoDato.STR
                resultado.valor = str(op1.valor) + str(op2.valor)

            # BOOLEAN/STR
            elif (op1.tipo == TipoDato.BOOLEAN or op1.tipo == TipoDato.STR) and (op2.tipo == TipoDato.BOOLEAN or op2.tipo == TipoDato.STR):
                resultado.tipo = TipoDato.STR
                resultado.valor = str(op1.valor) + str(op2.valor)
            
            # CHAR
            elif op1.tipo == TipoDato.CHAR and op2.tipo == TipoDato.CHAR:
                resultado.tipo = TipoDato.STR
                resultado.valor = str(ord(op1.valor) + ord(op2.valor))
            
            # CHAR/STR
            elif (op1.tipo == TipoDato.CHAR or op1.tipo == TipoDato.STR) and (op2.tipo == TipoDato.CHAR or op2.tipo == TipoDato.STR):
                resultado.tipo = TipoDato.STR
                resultado.valor = str(op1.valor) + str(op2.valor)
            
            # STR
            elif op1.tipo == TipoDato.STR and op2.tipo == TipoDato.STR:
                resultado.tipo = TipoDato.STR
                resultado.valor = op1.valor + op2.valor
            
            else:
                # Agregando a la tabla de errores
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar lo suma. La suma de los tipos no es permitida.')
                TablaErrores.addError(err)

        if self.operador == TipoAritmetica.RESTA:
            # INT
            if op1.tipo == TipoDato.INT and op2.tipo == TipoDato.INT:
                resultado.tipo = TipoDato.INT
                resultado.valor = op1.valor - op2.valor
            
            #INT/FLOAT
            elif (op1.tipo == TipoDato.INT or op1.tipo == TipoDato.FLOAT) and (op2.tipo == TipoDato.INT or op2.tipo == TipoDato.FLOAT):
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor - op2.valor
            
            #INT/CHAR
            elif (op1.tipo == TipoDato.INT or op1.tipo == TipoDato.CHAR) and (op2.tipo == TipoDato.INT or op2.tipo == TipoDato.CHAR):
                resultado.tipo = TipoDato.INT
                resultado.valor = ord(op1.valor) - ord(op2.valor)

            #FLOAT
            elif op1.tipo == TipoDato.FLOAT and op2.tipo == TipoDato.FLOAT:
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor - op2.valor
            
            # FLOAT/CHAR
            elif (op1.tipo == TipoDato.FLOAT or op1.tipo == TipoDato.CHAR) and (op2.tipo == TipoDato.FLOAT or op2.tipo == TipoDato.CHAR):
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = ord(op1.valor) - ord(op2.valor)
            
            else:
                # Agregando a la tabla de errores
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la resta. La resta de los tipos no es permitida.')
                TablaErrores.addError(err)
            
        if self.operador == TipoAritmetica.MULTIPLICACION:
            #INT
            if op1.tipo == TipoDato.INT and op2.tipo == TipoDato.INT:
                resultado.tipo = TipoDato.INT
                resultado.valor = op1.valor * op2.valor

            #INT/FLOAT
            elif (op1.tipo == TipoDato.INT or op1.tipo == TipoDato.FLOAT) and (op2.tipo == TipoDato.INT or op2.tipo == TipoDato.FLOAT):
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor * op2.valor

            #INT/CHAR
            elif (op1.tipo == TipoDato.INT or op1.tipo == TipoDato.CHAR) and (op2.tipo == TipoDato.INT or op2.tipo == TipoDato.CHAR):
                resultado.tipo = TipoDato.INT
                resultado.valor = ord(op1.valor) * ord(op2.valor)

            #FLOAT
            elif op1.tipo == TipoDato.FLOAT and op2.tipo == TipoDato.FLOAT:
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor * op2.valor
            
            # FLOAT/CHAR
            elif (op1.tipo == TipoDato.FLOAT or op1.tipo == TipoDato.CHAR) and (op2.tipo == TipoDato.FLOAT or op2.tipo == TipoDato.CHAR):
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = ord(op1.valor) * ord(op2.valor)
            
            else:
                # Agregando a la tabla de errores
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la multiplicación. La multiplicación de los tipos no es permitida.')
                TablaErrores.addError(err)

        if self.operador == TipoAritmetica.DIVISION:
            # INT
            if op1.tipo == TipoDato.INT and op2.tipo == TipoDato.INT:
                if op2.valor == 0:
                    # Agregando a la tabla de errores
                    err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la división. División por cero.')
                    TablaErrores.addError(err)
                    return resultado
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor // op2.valor
            
            #INT/FLOAT
            elif (op1.tipo == TipoDato.INT or op1.tipo == TipoDato.FLOAT) and (op2.tipo == TipoDato.INT or op2.tipo == TipoDato.FLOAT):
                if op2.valor == 0:
                    # Agregando a la tabla de errores
                    err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la división. División por cero.')
                    TablaErrores.addError(err)
                    return resultado
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor / op2.valor

            #INT/CHAR
            elif (op1.tipo == TipoDato.INT or op1.tipo == TipoDato.CHAR) and (op2.tipo == TipoDato.INT or op2.tipo == TipoDato.CHAR):
                if ord(op2.valor) == 0:
                    # Agregando a la tabla de errores
                    err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la división. División por cero.')
                    TablaErrores.addError(err)
                    return resultado
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = ord(op1.valor) / ord(op2.valor)

            #FLOAT
            elif op1.tipo == TipoDato.FLOAT and op2.tipo == TipoDato.FLOAT:
                if op2.valor == 0:
                    # Agregando a la tabla de errores
                    err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la división. División por cero.')
                    TablaErrores.addError(err)
                    return resultado
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor / op2.valor
            
            # FLOAT/CHAR
            elif (op1.tipo == TipoDato.FLOAT or op1.tipo == TipoDato.CHAR) and (op2.tipo == TipoDato.FLOAT or op2.tipo == TipoDato.CHAR):
                if ord(op2.valor) == 0:
                    # Agregando a la tabla de errores
                    err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la división. División por cero.')
                    TablaErrores.addError(err)
                    return resultado
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = ord(op1.valor) / ord(op2.valor)
            
            else:
                # Agregando a la tabla de errores
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la división. La división de los tipos no es permitida.')
                TablaErrores.addError(err)

        if self.operador == TipoAritmetica.POTENCIA: 
            # INT
            if op1.tipo == TipoDato.INT and op2.tipo == TipoDato.INT:
                resultado.tipo = TipoDato.INT
                resultado.valor = op1.valor ** op2.valor
            
            #INT/FLOAT
            elif (op1.tipo == TipoDato.INT or op1.tipo == TipoDato.FLOAT) and (op2.tipo == TipoDato.INT or op2.tipo == TipoDato.FLOAT):
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor ** op2.valor

            #FLOAT
            elif op1.tipo == TipoDato.FLOAT and op2.tipo == TipoDato.FLOAT:
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor ** op2.valor
            
            else:
                # Agregando a la tabla de errores
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la potencia. La potencia de los tipos no es permitida.')
                TablaErrores.addError(err)

        if self.operador == TipoAritmetica.MODULO:
            # INT
            if op1.tipo == TipoDato.INT and op2.tipo == TipoDato.INT:
                if op2.valor == 0:
                    # Agregando a la tabla de errores
                    err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar el módulo. División por cero.')
                    TablaErrores.addError(err)
                    return resultado
                resultado.tipo = TipoDato.INT
                resultado.valor = op1.valor % op2.valor
            
            #INT/FLOAT
            elif (op1.tipo == TipoDato.INT or op1.tipo == TipoDato.FLOAT) and (op2.tipo == TipoDato.INT or op2.tipo == TipoDato.FLOAT):
                if op2.valor == 0:
                    # Agregando a la tabla de errores
                    err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar el módulo. División por cero.')
                    TablaErrores.addError(err)
                    return resultado
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor % op2.valor

            #FLOAT
            elif op1.tipo == TipoDato.FLOAT and op2.tipo == TipoDato.FLOAT:
                if op2.valor == 0:
                    # Agregando a la tabla de errores
                    err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar el módulo. División por cero.')
                    TablaErrores.addError(err)
                    return resultado
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor % op2.valor
            
            else:
                # Agregando a la tabla de errores
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar el módulo. El módulo de los tipos no es permitida.')
                TablaErrores.addError(err)
            
        if self.operador == TipoAritmetica.NEGACION:
            # INT
            if op1.tipo == TipoDato.INT:
                resultado.tipo = TipoDato.INT
                resultado.valor = -op1.valor
            
            # FLOAT
            elif op1.tipo == TipoDato.FLOAT:
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = -op1.valor
            else:
                # Agregando a la tabla de errores
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la negación. El tipo {op1.tipo.name} no es permitido.')
                TablaErrores.addError(err)

        return resultado
    
    def recorrerArbol(self, raiz:Nodo):
        id = AST.generarId()
        tipo = ''
        if self.operador == TipoAritmetica.SUMA: tipo = '+'
        elif self.operador == TipoAritmetica.RESTA: tipo = '-'
        elif self.operador == TipoAritmetica.MULTIPLICACION: tipo = '*'
        elif self.operador == TipoAritmetica.DIVISION: tipo = '/'
        elif self.operador == TipoAritmetica.NEGACION: tipo = '-'
        elif self.operador == TipoAritmetica.POTENCIA: tipo = '^'
        elif self.operador == TipoAritmetica.MODULO: tipo = '%'
        hijo = Nodo(id=id, valor=tipo, hijos=[])
        raiz.addHijo(hijo)
        self.op1.recorrerArbol(hijo)
        if self.operador == TipoAritmetica.NEGACION:
            return
        self.op2.recorrerArbol(hijo)
    
    
    