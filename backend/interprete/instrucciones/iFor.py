from interprete.otros.enviroment import Enviroment
from .instruccion import Instruccion
from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato

class For(Instruccion):
    def __init__(self, text_val:str, inicializacion, condicion, incremento, instrucciones, linea:int, columna:int):
        super().__init__(text_val, linea, columna)
        self.inicializacion = inicializacion
        self.condicion = condicion
        self.incremento = incremento
        self.instrucciones = instrucciones

    def ejecutar(self, env:Enviroment):
        #incializacion del for
        #creamos un entorno para el for
        entorno_for = Enviroment(env, 'for')
        #ejecutamos la inicializacion
        if self.inicializacion:
            self.inicializacion.ejecutar(entorno_for)
        #utilizamos un while para la condicion del for
        while True:
            #verificamos la condicion
            resultado_cond = self.condicion.ejecutar(entorno_for)
            
            if resultado_cond.tipo != TipoDato.BOOLEAN or not resultado_cond.valor:
                break
            print(f"DEBUG: resultado_cond.tipo = {resultado_cond.tipo}, valor = {resultado_cond.valor}")
            #si la condicion del if  es verdadera entonces ejecutamos las instrucciones
            for instruccion in self.instrucciones:
                resultado = instruccion.ejecutar(entorno_for)
                if resultado == 'break':
                    return
                if resultado == 'continue':
                    break
                
            #ejecutamos la actualizacion
            if self.incremento:
                self.incremento.ejecutar(entorno_for)

    def recorrerArbol(self, raiz):
        id_for = AST.generarId()
        nodo_for = Nodo(id=id_for, valor='FOR', hijos=[])
        raiz.addHijo(nodo_for)

        # Inicialización
        id_init = AST.generarId()
        nodo_init = Nodo(id=id_init, valor='INICIALIZACION', hijos=[])
        nodo_for.addHijo(nodo_init)
        if self.inicializacion:
            self.inicializacion.recorrerArbol(nodo_init)

        # Condición
        id_cond = AST.generarId()
        nodo_cond = Nodo(id=id_cond, valor='CONDICION', hijos=[])
        nodo_for.addHijo(nodo_cond)
        if self.condicion:
            self.condicion.recorrerArbol(nodo_cond)

        # Incremento/Actualización
        id_inc = AST.generarId()
        nodo_inc = Nodo(id=id_inc, valor='INCREMENTO', hijos=[])
        nodo_for.addHijo(nodo_inc)
        if self.incremento:
            self.incremento.recorrerArbol(nodo_inc)

        # Instrucciones del cuerpo
        id_body = AST.generarId()
        nodo_body = Nodo(id=id_body, valor='INSTRUCCIONES', hijos=[])
        nodo_for.addHijo(nodo_body)
        for instruccion in getattr(self, 'instrucciones', []):
            instruccion.recorrerArbol(nodo_body)     
