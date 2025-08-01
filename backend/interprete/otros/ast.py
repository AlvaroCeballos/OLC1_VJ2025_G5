from subprocess import check_call
from types import NoneType
from interprete.otros.errores import TablaErrores, Error
from interprete.otros.consola import Consola

class Nodo:
    # id -> Identificador del dodo
    # valor -> Contenido del nodo
    # hijos -> Arreglo de 'n' hijos
    def __init__(self, id, valor:str, hijos):
        self.id = id
        self.valor = valor
        self.hijos = hijos
    
    def addHijo(self, nodoHijo):
        self.hijos.append(nodoHijo)
    
    def getId(self):
        return self.id
    
    def getValor(self):
        return self.valor
    
    def getHijos(self):
        return self.hijos
    
#Construye un arbol de sintaxis abstracto (AST) a partir de las instrucciones del programa. Y genera un archivo .dot y una imagen .png del AST.
class AST:
    id:int = 0
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
    
    def getAST(self):
        declaraciones = ''
        conexiones = ''
        raiz = Nodo(id=0, valor='INSTRUCCIONES', hijos=[])

        try:
            for instruccion in filter(None, self.instrucciones):
                instruccion.recorrerArbol(raiz)
        except TypeError as e:
                return
        declaraciones = f'\t{raiz.getId()} [label = "{raiz.getValor()}"];\n'
        declaraciones, conexiones = self.graficarArbol(raiz, declaraciones, conexiones)
        dot = 'digraph {\n' + declaraciones + conexiones + '}\n'
        
        filename = "backend/AST.dot"

        archivo = open(filename, "w")
        archivo.write(dot)
        archivo.close()
        
        check_call(['dot','-Tpng',filename,'-o', "backend/AST.png"])
        Consola.addConsola('AST generado con éxito.')
        return {'dot': dot}

    def graficarArbol(self, raiz:Nodo, declaraciones:str, conexiones:str):
        for hijo in raiz.getHijos():
            declaraciones += f'\t{hijo.getId()} [label = "{hijo.getValor()}"];\n'
            conexiones += f'\t{raiz.getId()} -> {hijo.getId()};\n'
            declaraciones, conexiones = self.graficarArbol(hijo, declaraciones, conexiones)
        return declaraciones, conexiones

    @classmethod
    def generarId(cls):
        cls.id += 1
        return cls.id