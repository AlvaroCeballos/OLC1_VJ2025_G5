from interprete.otros.enviroment import Enviroment
from .instruccion import Instruccion
from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato
from interprete.instrucciones.iCase import Case
from interprete.instrucciones.iBrake import Break
from interprete.otros.errores import Error, TablaErrores  # ← AGREGAR IMPORT

class Switch(Instruccion):
    contador_global = 0  # ← AGREGAR contador global como en while/do-while

    def __init__(self, text_val: str, condicion, casos, default, linea: int, columna: int):
        super().__init__(text_val, linea, columna)
        self.condicion = condicion
        self.casos = casos if casos is not None else []
        self.default = default if default is not None else []

    def ejecutar(self, env: Enviroment):
        # Incrementar contador y crear nombre único como en while/do-while
        Switch.contador_global += 1
        nombre_switch = f"switch{Switch.contador_global}"
        
        # Crear nuevo entorno para el switch
        entorno_switch = Enviroment(env, nombre_switch)
        
        print(f"DEBUG: Creando {nombre_switch} con entorno padre: {env.ambito}")
        
        # Evaluar condición en el entorno del switch
        valor_switch = self.condicion.ejecutar(entorno_switch)
        
        # Validación de tipo entero
        if valor_switch.tipo != TipoDato.INT:
            err = Error(
                tipo='Semántico',
                linea=self.linea,
                columna=self.columna,
                descripcion='La expresión del switch debe ser de tipo entero.'
            )
            TablaErrores.addError(err)
            return

        encontrado = False
        
        # Buscar case que coincida
        for case in self.casos:
            valor_case = case.condicion.ejecutar(entorno_switch)  # ← Usar entorno_switch
            
            if valor_case.valor == valor_switch.valor:
                encontrado = True
                
                # Validar break obligatorio
                if not case.instrucciones or not isinstance(case.instrucciones[-1], Break):
                    err = Error(
                        tipo='Semántico',
                        linea=case.linea,
                        columna=case.columna,
                        descripcion='Cada case debe terminar con break.'
                    )
                    TablaErrores.addError(err)
                    return
                
                # Ejecutar instrucciones del case en el entorno del switch
                print(f"DEBUG: Ejecutando case {valor_case.valor} en {nombre_switch}")
                for instruccion in (case.instrucciones if case.instrucciones is not None else []):
                    resultado = instruccion.ejecutar(entorno_switch)  # ← Usar entorno_switch
                    if resultado == 'break':
                        print(f"DEBUG: Break encontrado, saliendo de {nombre_switch}")
                        print(f"DEBUG: Terminando {nombre_switch}")
                        return
                
                print(f"DEBUG: Terminando {nombre_switch}")
                return  # Solo ejecuta el primer case que coincide

        # Si ningún case coincide, ejecuta default si existe
        if not encontrado and self.default:
            print(f"DEBUG: Ejecutando default en {nombre_switch}")
            for instruccion in (self.default if self.default is not None else []):
                resultado = instruccion.ejecutar(entorno_switch)  # ← Usar entorno_switch
                if resultado == 'break':
                    print(f"DEBUG: Break en default, saliendo de {nombre_switch}")
                    break
        
        print(f"DEBUG: Terminando {nombre_switch}")
        return self

    def recorrerArbol(self, raiz):
        id_switch = AST.generarId()
        nodo_switch = Nodo(id=id_switch, valor='SWITCH', hijos=[])
        raiz.addHijo(nodo_switch)

        # Nodo de la expresión del switch
        id_expr = AST.generarId()
        nodo_expr = Nodo(id=id_expr, valor='EXPRESION', hijos=[])
        nodo_switch.addHijo(nodo_expr)
        self.condicion.recorrerArbol(nodo_expr)

        # Nodos de los cases
        for case in self.casos:
            case.recorrerArbol(nodo_switch)

        # Nodo default (si existe)
        if self.default:
            id_default = AST.generarId()
            nodo_default = Nodo(id=id_default, valor='DEFAULT', hijos=[])
            nodo_switch.addHijo(nodo_default)
            for instruccion in self.default:
                instruccion.recorrerArbol(nodo_default)
    
    # Resetear el contador global de switch (como en while/do-while)
    @classmethod
    def reset_contador(cls):
        cls.contador_global = 0