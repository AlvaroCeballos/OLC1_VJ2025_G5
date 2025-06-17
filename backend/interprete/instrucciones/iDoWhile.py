from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato
from .instruccion import Instruccion
from interprete.otros.enviroment import Enviroment
from interprete.otros.errores import Error, TablaErrores

class DoWhile(Instruccion):
    contador_global = 0  # Contador global para llevar control de los do-while anidados
    
    def __init__(self, text_val:str, instrucciones, condicion, linea, columna):
        super().__init__(text_val, linea, columna)
        # Nota: instrucciones ANTES que condicion (diferente al while normal)
        self.instrucciones = instrucciones
        self.condicion = condicion
    
    def ejecutar(self, env:Enviroment):
        # Incrementa el contador de los do-while y va creando nombres para identificar los scopes
        DoWhile.contador_global += 1
        nombre_dowhile = f"dowhile{DoWhile.contador_global}"
        
        # Crear nuevo entorno para el do-while
        entorno_dowhile = Enviroment(env, nombre_dowhile)
        
        print(f"DEBUG: Creando {nombre_dowhile} con entorno padre: {env.ambito}")
        
        # DO-WHILE siempre ejecuta AL MENOS UNA VEZ
        while True:
            # Ejecutar instrucciones del do-while PRIMERO (diferencia clave)
            for instruccion in self.instrucciones:
                resultado = instruccion.ejecutar(entorno_dowhile)
            
            # DESPUÉS evaluar la condición
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
    
    # Función para recorrer el árbol de sintaxis abstracta
    def recorrerArbol(self, raiz:Nodo):
        id = AST.generarId()
        hijo = Nodo(id=id, valor='DO-WHILE', hijos=[])
        raiz.addHijo(hijo)
        
        # Agregar nodo de instrucciones PRIMERO
        id = AST.generarId()
        nodo_instrucciones = Nodo(id=id, valor='INSTRUCCIONES', hijos=[])
        hijo.addHijo(nodo_instrucciones)
        
        for instruccion in self.instrucciones:
            instruccion.recorrerArbol(nodo_instrucciones)
        
        # Agregar nodo de condición DESPUÉS
        id = AST.generarId()
        nodo_condicion = Nodo(id=id, valor='CONDICION', hijos=[])
        hijo.addHijo(nodo_condicion)
        self.condicion.recorrerArbol(nodo_condicion)
    
    # Resetear el contador global de do-while
    @classmethod
    def reset_contador(cls):
        cls.contador_global = 0