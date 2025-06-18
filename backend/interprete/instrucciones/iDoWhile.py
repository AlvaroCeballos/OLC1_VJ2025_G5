from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato
from .instruccion import Instruccion
from interprete.otros.enviroment import Enviroment
from interprete.otros.errores import Error, TablaErrores

class DoWhile(Instruccion):
    contador_global = 0  
    
    def __init__(self, text_val:str, instrucciones, condicion, linea, columna):
        super().__init__(text_val, linea, columna)
        # A diferencia del while, el atributo de instrucciones va antes de la condicion
        self.instrucciones = instrucciones
        self.condicion = condicion
    
    def ejecutar(self, env:Enviroment):
        # Incrementa el contador de los do-while y va creando nombres para identificar los scopes
        DoWhile.contador_global += 1
        nombre_dowhile = f"dowhile{DoWhile.contador_global}"
        
        # Crear nuevo entorno para el do-while
        entorno_dowhile = Enviroment(env, nombre_dowhile)
        
        print(f"DEBUG: Creando {nombre_dowhile} con entorno padre: {env.ambito}")
        
        # Se ejecuta como minimo 1 vez
        while True:
            # Se ejecutan primero las instrucciones
            for instruccion in self.instrucciones:
                resultado = instruccion.ejecutar(entorno_dowhile)
            
            #Se evalúa la condición después de ejecutar las instrucciones
            resultado_condicion = self.condicion.ejecutar(entorno_dowhile)
            
            # Validar que la condición sea booleana
            if resultado_condicion.tipo != TipoDato.BOOLEAN:
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, 
                          descripcion=f'La condición del do-while debe ser de tipo boolean')
                TablaErrores.addError(err)
                break
            
            # Si la condición es falsa, salir del ciclo do-while
            if not resultado_condicion.valor:
                break
        
        print(f"DEBUG: Terminando {nombre_dowhile}")
        return self
    
    def recorrerArbol(self, raiz:Nodo):
        id = AST.generarId()
        hijo = Nodo(id=id, valor='DO-WHILE', hijos=[])
        raiz.addHijo(hijo)
        
        # Se agrega primero el nodo de instrucciones
        id = AST.generarId()
        nodo_instrucciones = Nodo(id=id, valor='INSTRUCCIONES', hijos=[])
        hijo.addHijo(nodo_instrucciones)
        
        for instruccion in self.instrucciones:
            instruccion.recorrerArbol(nodo_instrucciones)
        
        # Se agrega el nodo de la condicion
        id = AST.generarId()
        nodo_condicion = Nodo(id=id, valor='CONDICION', hijos=[])
        hijo.addHijo(nodo_condicion)
        self.condicion.recorrerArbol(nodo_condicion)
    
    # Resetear el contador global de do-while
    @classmethod
    def reset_contador(cls):
        cls.contador_global = 0