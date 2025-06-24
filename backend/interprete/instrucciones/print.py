from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato
from .instruccion import Instruccion
from interprete.otros.enviroment import Enviroment
from interprete.otros.consola import Consola
from interprete.otros.errores import Error, TablaErrores


class Print(Instruccion):
    def __init__(self, text_val:str, argumento, linea, columna):
        super().__init__(text_val, linea, columna)
        self.text_val = text_val
        self.argumento = argumento
    
    def ejecutar(self, env:Enviroment):
        exp = self.argumento.ejecutar(env)

        # Validar que no haya un error en la expresion
        if exp.tipo == TipoDato.ERROR:
            TablaErrores.addError(Error(
                tipo='Semántico',
                descripcion='Error en la expresión de la función println()',
                linea=self.linea,
                columna=self.columna
            ))
            return self
            
        Consola.addConsola(exp.valor)
        print(f'Consola: {exp.valor}')

        return self

    
    def recorrerArbol(self, raiz:Nodo):
        id = AST.generarId()
        hijo = Nodo(id=id, valor='PRINTLN', hijos=[])
        raiz.addHijo(hijo)                                    
        self.argumento.recorrerArbol(hijo)
    