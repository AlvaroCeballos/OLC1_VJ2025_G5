from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato
from .instruccion import Instruccion
from interprete.otros.enviroment import Enviroment
from interprete.otros.errores import Error, TablaErrores

class While(Instruccion):
    contador_global = 0  # Contador global para llevar control de los while anidados
    
    def __init__(self, text_val:str, condicion, instrucciones, linea, columna):
        super().__init__(text_val, linea, columna)
        #se crean como parametros las instrucciones y la condicion
        self.condicion = condicion
        self.instrucciones = instrucciones
    
    def ejecutar(self, env:Enviroment):
        entorno_while = Enviroment(env, 'while', 'while')
        # Incrementa el contador de los while y va creando nombres para identificar los scopes
        While.contador_global += 1
        nombre_while = f"while {While.contador_global}"
        
        # Crear nuevo entorno para el while
        entorno_while = Enviroment(env, nombre_while)
        
        print(f"DEBUG: Creando {nombre_while} con entorno padre: {env.ambito}")
        
        while True:
            # Se ejecuta la condición del while del entorno actual
            resultado_condicion = self.condicion.ejecutar(entorno_while)
            
            # Validar que la condición sea booleana
            if resultado_condicion.tipo != TipoDato.BOOL:
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, 
                          descripcion=f'La condición del while debe ser de tipo boolean')
                TablaErrores.addError(err)
                break
            
            # Si la condición es falsa, salir del ciclo while
            if not resultado_condicion.valor:
                break
            
            # Ejecutar instrucciones del while
            for instruccion in self.instrucciones:
                resultado = instruccion.ejecutar(entorno_while)
                if resultado == 'break':
                    return
                if resultado == 'continue':
                    break  # Sale del for, pero sigue el while
        
        print(f"DEBUG: Terminando {nombre_while}")
        return self
    
    #función para recorrer el arbol de sintaxis abstracta
    def recorrerArbol(self, raiz:Nodo):
        id = AST.generarId()
        hijo = Nodo(id=id, valor='WHILE', hijos=[])
        raiz.addHijo(hijo)
        
        # Agregar nodo de condición
        id = AST.generarId()
        nodo_condicion = Nodo(id=id, valor='CONDICION', hijos=[])
        hijo.addHijo(nodo_condicion)
        self.condicion.recorrerArbol(nodo_condicion)
        
        # Agregar nodo de instrucciones
        id = AST.generarId()
        nodo_instrucciones = Nodo(id=id, valor='INSTRUCCIONES', hijos=[])
        hijo.addHijo(nodo_instrucciones)
        
        for instruccion in self.instrucciones:
            instruccion.recorrerArbol(nodo_instrucciones)
    
    #resetear el contador global de while
    @classmethod
    def reset_contador(cls):
        cls.contador_global = 0