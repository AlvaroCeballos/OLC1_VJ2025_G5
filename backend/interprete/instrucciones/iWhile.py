from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato
from .instruccion import Instruccion
from interprete.otros.enviroment import Enviroment
from interprete.otros.errores import Error, TablaErrores

class While(Instruccion):
    contador_global = 0  # Contador global simple
    
    def __init__(self, text_val:str, condicion, instrucciones, linea, columna):
        super().__init__(text_val, linea, columna)
        self.condicion = condicion
        self.instrucciones = instrucciones
    
    def ejecutar(self, env:Enviroment):
        # Incrementar contador y crear nombre único
        While.contador_global += 1
        nombre_while = f"while{While.contador_global}"
        
        # Crear nuevo entorno para el while
        entorno_while = Enviroment(env, nombre_while)
        
        print(f"DEBUG: Creando {nombre_while} con entorno padre: {env.ambito}")
        
        while True:
            # Evaluar condición
            resultado_condicion = self.condicion.ejecutar(entorno_while)
            
            # Validar que la condición sea booleana
            if resultado_condicion.tipo != TipoDato.BOOLEAN:
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, 
                          descripcion=f'La condición del while debe ser de tipo boolean')
                TablaErrores.addError(err)
                break
            
            # Si la condición es falsa, salir del ciclo
            if not resultado_condicion.valor:
                break
            
            # Ejecutar instrucciones del while
            for instruccion in self.instrucciones:
                print(f"DEBUG: Ejecutando instrucción en {nombre_while}: {type(instruccion).__name__}")
                resultado = instruccion.ejecutar(entorno_while)
        
        print(f"DEBUG: Terminando {nombre_while}")
        return self
    
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
    
    @classmethod
    def reset_contador(cls):
        cls.contador_global = 0