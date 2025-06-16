from interprete.instrucciones.instruccion import Instruccion
from interprete.otros.ast import AST, Nodo
from interprete.otros.enviroment import Enviroment
from interprete.otros.errores import Error, TablaErrores
from interprete.otros.retorno import Retorno
from interprete.otros.tipos import TipoDato

class Instruccion_if(Instruccion):
    contador_global = 0  # Contador global para llevar control de los if anidados

    def __init__(self, text_val: str, condicion, instrucciones_if, instrucciones_else=None, linea: int = 0, columna: int = 0):
        super().__init__(text_val, linea, columna)
        self.condicion = condicion                       # Expresión booleana
        self.instrucciones_if = instrucciones_if         # Lista de instrucciones para el bloque "if"
        self.instrucciones_else = instrucciones_else     # None, lista o instancia de If para "else"/"else if"

    def ejecutar(self, env: Enviroment):
        Instruccion_if.contador_global += 1
        nombre_if = f"if {Instruccion_if.contador_global}"
        env_if = Enviroment(ent_anterior=env, ambito=nombre_if)
        
        # Ejecutar la condición del if
        resultado = self.condicion.ejecutar(env)
        if resultado.tipo != TipoDato.BOOLEAN:
            err = Error(
                tipo='Semántico',
                linea=self.linea,
                columna=self.columna,
                descripcion='Condición de if no es booleana.'
            )
            TablaErrores.addError(err)
            return self

        # Ejecutar bloque "if"
        if resultado.valor:
            for instr in self.instrucciones_if:
                instr.ejecutar(env_if)
        elif self.instrucciones_else:
            # Manejar ELSE como un nuevo entorno
            nombre_else = f"{nombre_if} else"
            env_else = Enviroment(ent_anterior=env, ambito=nombre_else)
            
            
            if isinstance(self.instrucciones_else, list):
                for instr in self.instrucciones_else:
                    instr.ejecutar(env_else)
            # Si es otra instrucción (p.ej. otro If para "else if")
            else:
                self.instrucciones_else.ejecutar(env_else)

        return self

    def recorrerArbol(self, raiz: Nodo):
        id_root = AST.generarId()
        nodo_if = Nodo(id=id_root, valor='IF', hijos=[])
        raiz.addHijo(nodo_if)

        # Condición
        self.condicion.recorrerArbol(nodo_if)

        # Bloque IF
        for instr in self.instrucciones_if:
            instr.recorrerArbol(nodo_if)

        # Bloque ELSE / ELSE IF
        if self.instrucciones_else:
            # Si es una lista: ELSE bloque
            if isinstance(self.instrucciones_else, list):
                id_else = AST.generarId()
                nodo_else = Nodo(id=id_else, valor='ELSE', hijos=[])
                raiz.addHijo(nodo_else)
                for instr in self.instrucciones_else:
                    instr.recorrerArbol(nodo_else)
            # Si es una sola instrucción (otro If): ELSE IF
            else:
                id_eif = AST.generarId()
                nodo_eif = Nodo(id=id_eif, valor='ELSE_IF', hijos=[])
                raiz.addHijo(nodo_eif)
                self.instrucciones_else.recorrerArbol(nodo_eif)
