from interprete.otros.enviroment import Enviroment
from .instruccion import Instruccion
from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato
from interprete.instrucciones.iCase import Case
from interprete.instrucciones.iBrake import Break


class Switch(Instruccion):

    def __init__(self, text_val: str, condicion, casos, default, linea: int, columna: int):
        super().__init__(text_val, linea, columna)
        self.condicion = condicion
        self.casos = casos if casos is not None else []
        self.default = default if default is not None else []

    def ejecutar(self, env: Enviroment):
        entorno_switch = Enviroment(env, 'switch', 'switch')
        valor_switch = self.condicion.ejecutar(env)
        # Validación de tipo entero
        if valor_switch.tipo != TipoDato.INT:
            TablaErrores.addError(Error(
                tipo='Semántico',
                linea=self.linea,
                columna=self.columna,
                descripcion='La expresión del switch debe ser de tipo entero.'
            ))
            return

        encontrado = False
        for case in self.casos:
            valor_case = case.condicion.ejecutar(env)
            if valor_case.valor == valor_switch.valor:
                encontrado = True
                # Validar break obligatorio
                if not case.instrucciones or not isinstance(case.instrucciones[-1], Break):
                    TablaErrores.addError(Error(
                        tipo='Semántico',
                        linea=case.linea,
                        columna=case.columna,
                        descripcion='Cada case debe terminar con break.'
                    ))
                    return
                # Ejecutar instrucciones del case
                for instruccion in (case.instrucciones if case.instrucciones is not None else []):
                    resultado = instruccion.ejecutar(env)
                    if resultado == 'break':
                        return
                return  # Solo ejecuta el primer case que coincide

        # Si ningún case coincide, ejecuta default si existe
        if not encontrado and self.default:
            for instruccion in (self.default if self.default is not None else []):
                resultado = instruccion.ejecutar(env)
                if resultado == 'break':
                    return

                
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