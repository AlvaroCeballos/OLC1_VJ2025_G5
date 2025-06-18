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

        def get_valor_ascii(valor, tipo):
            if tipo == TipoDato.CHAR:
                return ord(valor)
            return valor  
            
        resultado = Retorno(tipo=TipoDato.ERROR, valor=None)

        if self.operador == TipoAritmetica.NEGACION:
            op = self.op2.ejecutar(env)
            if op.tipo == TipoDato.INT:
                resultado.tipo = TipoDato.INT
                resultado.valor = -op.valor
            elif op.tipo == TipoDato.FLOAT:
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = -op.valor
            else:
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna,
                            descripcion=f'Error al realizar la negación. El tipo {op.tipo.name} no es permitido.')
                TablaErrores.addError(err)
            return resultado
        
        op1:Retorno = self.op1.ejecutar(env)
        op2:Retorno = self.op2.ejecutar(env)
        # Que no haya error en los operandos
        if op1.tipo == TipoDato.ERROR or op2.tipo == TipoDato.ERROR:
            # Agregando a la tabla de errores
            err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la operación aritmética.')
            TablaErrores.addError(err)
            return resultado
    
        if self.operador == TipoAritmetica.SUMA:
            # --- BLOQUE PARA BOOLEANOS ---
            if op1.tipo == TipoDato.BOOL or op2.tipo == TipoDato.BOOL:
                # Solo permitir concatenación con string
                if op1.tipo == TipoDato.STR or op2.tipo == TipoDato.STR:
                    resultado.tipo = TipoDato.STR
                    resultado.valor = str(op1.valor) + str(op2.valor)
                else:
                    # Error: suma no permitida con booleanos
                    resultado.tipo = TipoDato.ERROR
                    resultado.valor = None
                    err = Error(
                        tipo='Semántico',
                        linea=self.linea,
                        columna=self.columna,
                        descripcion='Error al realizar lo suma. La suma de los tipos no es permitida.'
                    )
                    TablaErrores.addError(err)
                return resultado

            # INT
            if op1.tipo == TipoDato.INT and op2.tipo == TipoDato.INT:
                resultado.tipo = TipoDato.INT
                resultado.valor = op1.valor + op2.valor
            
            # INT/FLOAT
            elif (op1.tipo == TipoDato.INT or op1.tipo == TipoDato.FLOAT) and (op2.tipo == TipoDato.INT or op2.tipo == TipoDato.FLOAT):
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor + op2.valor

            # CHAR + CHAR (concatenación)
            elif op1.tipo == TipoDato.CHAR and op2.tipo == TipoDato.CHAR:
                resultado.tipo = TipoDato.STR
                resultado.valor = op1.valor + op2.valor
            
            # INT/CHAR (suma ASCII)
            elif (op1.tipo == TipoDato.INT and op2.tipo == TipoDato.CHAR) or (op1.tipo == TipoDato.CHAR and op2.tipo == TipoDato.INT):
                resultado.tipo = TipoDato.INT
                resultado.valor = get_valor_ascii(op1.valor, op1.tipo) + get_valor_ascii(op2.valor, op2.tipo)
            
            # INT/STR
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
                resultado.valor = get_valor_ascii(op1.valor, op1.tipo) + get_valor_ascii(op2.valor, op2.tipo)
            
            # FLOAT/STR
            elif (op1.tipo == TipoDato.FLOAT or op1.tipo == TipoDato.STR) and (op2.tipo == TipoDato.FLOAT or op2.tipo == TipoDato.STR):
                resultado.tipo = TipoDato.STR
                resultado.valor = str(op1.valor) + str(op2.valor)

            # CHAR
            elif op1.tipo == TipoDato.CHAR and op2.tipo == TipoDato.CHAR:
                resultado.tipo = TipoDato.STR
                resultado.valor = op1.valor + op2.valor
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

            # CHAR - CHAR: ERROR
            if op1.tipo == TipoDato.CHAR and op2.tipo == TipoDato.CHAR:
                resultado.tipo = TipoDato.ERROR
                resultado.valor = None
                err = Error(
                    tipo='Semántico',
                    linea=self.linea,
                    columna=self.columna,
                    descripcion='Error al realizar la resta. La resta de los tipos no es permitida.'
                )
                TablaErrores.addError(err)
                return resultado
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
                resultado.valor = get_valor_ascii(op1.valor, op1.tipo) - get_valor_ascii(op2.valor, op2.tipo)

            #FLOAT
            elif op1.tipo == TipoDato.FLOAT and op2.tipo == TipoDato.FLOAT:
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor - op2.valor
            
            # FLOAT/CHAR
            elif (op1.tipo == TipoDato.FLOAT or op1.tipo == TipoDato.CHAR) and (op2.tipo == TipoDato.FLOAT or op2.tipo == TipoDato.CHAR):
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = get_valor_ascii(op1.valor, op1.tipo) - get_valor_ascii(op2.valor, op2.tipo)
            
            else:
                # Agregando a la tabla de errores
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la resta. La resta de los tipos no es permitida.')
                TablaErrores.addError(err)
            
        if self.operador == TipoAritmetica.MULTIPLICACION:

            # CHAR * CHAR: ERROR
            if op1.tipo == TipoDato.CHAR and op2.tipo == TipoDato.CHAR:
                resultado.tipo = TipoDato.ERROR
                resultado.valor = None
                err = Error(
                    tipo='Semántico',
                    linea=self.linea,
                    columna=self.columna,
                    descripcion='Error al realizar la multiplicación. La multiplicación de los tipos no es permitida.'
                )
                TablaErrores.addError(err)
                return resultado
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
                resultado.valor = get_valor_ascii(op1.valor, op1.tipo) * get_valor_ascii(op2.valor, op2.tipo)

            #FLOAT
            elif op1.tipo == TipoDato.FLOAT and op2.tipo == TipoDato.FLOAT:
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor * op2.valor
            
            # FLOAT/CHAR
            elif (op1.tipo == TipoDato.FLOAT or op1.tipo == TipoDato.CHAR) and (op2.tipo == TipoDato.FLOAT or op2.tipo == TipoDato.CHAR):
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = get_valor_ascii(op1.valor, op1.tipo) * get_valor_ascii(op2.valor, op2.tipo)
            
            else:
                # Agregando a la tabla de errores
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la multiplicación. La multiplicación de los tipos no es permitida.')
                TablaErrores.addError(err)

        if self.operador == TipoAritmetica.DIVISION:

            # CHAR / CHAR: ERROR 
            if op1.tipo == TipoDato.CHAR and op2.tipo == TipoDato.CHAR:
                resultado.tipo = TipoDato.ERROR
                resultado.valor = None
                err = Error(
                    tipo='Semántico',
                    linea=self.linea,
                    columna=self.columna,
                    descripcion='Error al realizar la división. La división de los tipos no es permitida.'
                )
                TablaErrores.addError(err)
                return resultado
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

            # INT/CHAR y CHAR/INT
            elif (op1.tipo == TipoDato.INT and op2.tipo == TipoDato.CHAR) or (op1.tipo == TipoDato.CHAR and op2.tipo == TipoDato.INT):
                divisor = get_valor_ascii(op2.valor, op2.tipo)
                if divisor == 0:
                    # error...
                    err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la división. División por cero.')
                    TablaErrores.addError(err)
                    return resultado
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = get_valor_ascii(op1.valor, op1.tipo) / divisor

            #FLOAT
            elif op1.tipo == TipoDato.FLOAT and op2.tipo == TipoDato.FLOAT:
                if op2.valor == 0:
                    # Agregando a la tabla de errores
                    err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la división. División por cero.')
                    TablaErrores.addError(err)
                    return resultado
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = op1.valor / op2.valor
            
            # FLOAT/CHAR y CHAR/FLOAT
            elif (op1.tipo == TipoDato.FLOAT and op2.tipo == TipoDato.CHAR) or (op1.tipo == TipoDato.CHAR and op2.tipo == TipoDato.FLOAT):
                divisor = get_valor_ascii(op2.valor, op2.tipo)
                if divisor == 0:
                    # error...
                    err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, descripcion=f'Error al realizar la división. División por cero.')
                    TablaErrores.addError(err)
                    return resultado
                resultado.tipo = TipoDato.FLOAT
                resultado.valor = get_valor_ascii(op1.valor, op1.tipo) / divisor
                        
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
        if self.operador == TipoAritmetica.NEGACION:
            if self.op2 is not None:
                self.op2.recorrerArbol(hijo)
            return
        if self.op1 is not None:
            self.op1.recorrerArbol(hijo)
        if self.op2 is not None:
            self.op2.recorrerArbol(hijo)
    
    
    