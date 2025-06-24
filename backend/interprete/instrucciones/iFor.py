from interprete.otros.enviroment import Enviroment
from .instruccion import Instruccion
from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato
from interprete.otros.errores import Error, TablaErrores  # ← AGREGAR IMPORT

class For(Instruccion):
    contador_global = 0  # ← AGREGAR contador global como en while/do-while/switch

    def __init__(self, text_val:str, inicializacion, condicion, incremento, instrucciones, linea:int, columna:int):
        super().__init__(text_val, linea, columna)
        self.inicializacion = inicializacion
        self.condicion = condicion
        self.incremento = incremento
        self.instrucciones = instrucciones

    def ejecutar(self, env:Enviroment):
        # Incrementar contador y crear nombre único como en while/do-while/switch
        For.contador_global += 1
        nombre_for = f"for{For.contador_global}"
        
        # Crear nuevo entorno para el for
        entorno_for = Enviroment(env, nombre_for)
        
        #print(f"DEBUG: Creando {nombre_for} con entorno padre: {env.ambito}")
        
        # Ejecutar la inicialización en el entorno del for
        if self.inicializacion:
            #print(f"DEBUG: Ejecutando inicialización en {nombre_for}")
            self.inicializacion.ejecutar(entorno_for)
        
        # Ciclo principal del for
        while True:
            # Evaluar condición en el entorno del for
            resultado_cond = self.condicion.ejecutar(entorno_for)
            
            # Validar que la condición sea booleana
            if resultado_cond.tipo != TipoDato.BOOL:
                err = Error(
                    tipo='Semántico',
                    linea=self.linea,
                    columna=self.columna,
                    descripcion='La condición del for debe ser de tipo boolean'
                )
                TablaErrores.addError(err)
                break
            
            # Si la condición es falsa, salir del for
            if not resultado_cond.valor:
                #print(f"DEBUG: Condición falsa, saliendo de {nombre_for}")
                break
            
            # Ejecutar instrucciones del cuerpo del for
            for instruccion in (self.instrucciones if self.instrucciones is not None else []):
                resultado = instruccion.ejecutar(entorno_for)
                if resultado == 'break':
                    #print(f"DEBUG: Break encontrado, saliendo de {nombre_for}")
                    #print(f"DEBUG: Terminando {nombre_for}")
                    return  # Sale completamente del ciclo
                if resultado == 'continue':
                    #print(f"DEBUG: Continue encontrado, siguiente iteración de {nombre_for}")
                    break  # Sale del for interno, pero sigue con la siguiente iteración del while
            
            # Ejecutar la actualización solo si no hubo break
            if self.incremento:
                #print(f"DEBUG: Ejecutando incremento en {nombre_for}")
                self.incremento.ejecutar(entorno_for)
        
        #print(f"DEBUG: Terminando {nombre_for}")
        return self

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
        for instruccion in (self.instrucciones if self.instrucciones is not None else []):
            instruccion.recorrerArbol(nodo_body)
    
    # Resetear el contador global de for (como en while/do-while/switch)
    @classmethod
    def reset_contador(cls):
        cls.contador_global = 0