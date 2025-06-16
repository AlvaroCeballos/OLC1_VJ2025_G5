from interprete.otros.enviroment import Enviroment
from .instruccion import Instruccion
from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato


class Switch(Instruccion):

    def __init__(self, text_val: str, condicion, casos, default, linea: int, columna : int):
        super().__init__(text_val, linea, columna)
        self.condicion = condicion
        self.casos = casos #lista de casos
        self.default = default #instruciones por defecto

    def ejecutar(self, env: Enviroment):
        #condicion del switch
        resultado_switch = self.condicion.ejecutar(env)
        #se crea un entorno switch
        entorno_switch =Enviroment(env, 'switch')
        encontrado = False

        print(f"DEBUG: Creando {'switch'} con entorno padre: {env.ambito}")

        for case in self.casos:
            valor_case = case.condicion.ejecutar(entorno_switch)
            if encontrado or valor_case.valor == resultado_switch.valor:
                #si encuentra el case, creamor un entorno para el case
                entorno_case = Enviroment(entorno_switch, 'case')
                print(f"DEBUG: Creando {'case'} con entorno padre: {entorno_switch.ambito}")
                encontrado = True
                resultado = case.ejecutar(entorno_case)
                if resultado == 'break':
                    return
                
        if not encontrado and self.default:
            #no encontramos el case entonces ejecutamos el default
            #tambien creamos un entorno para el default
            entorno_default = Enviroment(entorno_switch, 'default')
            print(f"DEBUG: Creando {'default'} con entorno padre: {entorno_switch.ambito}")
            for instruccion in self.default:
                resultado = instruccion.ejecutar(entorno_default)
                if resultado =='break':
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