from analizadores.parser import parser
from interprete.otros.enviroment import Enviroment
from interprete.otros.ast import AST
from interprete.otros.consola import Consola
from interprete.otros.errores import TablaErrores
from interprete.instrucciones.iWhile import While
from interprete.instrucciones.iDoWhile import DoWhile
f = open('backend/entradaDoWhile.txt', 'r', encoding='utf-8')
data = f.read()

While.reset_contador()
DoWhile.reset_contador() 
instrucciones = parser.parse(data.lower())
env = Enviroment(ent_anterior=None, ambito='Global')
try:
    for instruccion in instrucciones:
        instruccion.ejecutar(env)
except Exception as e:
    print(f"Error inesperado: {e}")

print('TABLA DE ERRORES:')
print(TablaErrores.serializarTBErrores())
print('TABLA DE SIMBOLOS:')
print(Enviroment.serializarTodosSimbolos())

ast = AST(instrucciones)
ast.getAST()

Enviroment.cleanEnviroments()
TablaErrores.cleanTablaErrores()