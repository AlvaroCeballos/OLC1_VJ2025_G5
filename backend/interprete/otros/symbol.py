from interprete.otros.tipos import *

class Symbol:
    def __init__(self, tipo_simbolo:TipoSimbolo=None, tipo:TipoDato=None, id:str='', valor='', ambito:str='', parametros=[], instrucciones=[], direccion:int=''):
        self.tipo_simbolo = tipo_simbolo        # Si es variable, funcion
        self.tipo = tipo                        # Para el tipo de dato o tipo de dato que retorna una funcion
        self.id = id                            # Nombre del simbolo
        self.valor = valor                      # Para el caso de las variables, su valor
        self.ambito = ambito                    # En que scope se encuentra
        self.parametros = parametros            # Para el caso de funciones
        self.instrucciones = instrucciones      # Para el caso de funciones y sus instrucciones

    # Los parametros son un arreglo de declaraciones, y cada declaracion tiene el atributo 'id'
    def serializarParametros(self):
        text = ''
        if self.parametros == None:
            return text
        for i in range(len(self.parametros)):
            if i == len(self.parametros) - 1:
                text += self.parametros[i].id
            else:
                text += self.parametros[i].id + ', '
        return text