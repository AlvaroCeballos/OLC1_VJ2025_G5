from analizadores.parser import parser
from analizadores.lexer import lexer
from interprete.otros.enviroment import Enviroment
from interprete.otros.ast import AST
from interprete.otros.consola import Consola
from interprete.otros.errores import TablaErrores
from interprete.instrucciones.iWhile import While
from interprete.instrucciones.iDoWhile import DoWhile
f = open('backend/entrada.txt', 'r', encoding='utf-8')
data = f.read()

While.reset_contador()
DoWhile.reset_contador() 
lexer.lineno = 1
instrucciones = parser.parse(data, lexer=lexer)
env = Enviroment(ent_anterior=None, ambito='Global')
if instrucciones is None:
    instrucciones = []
try:
    for instruccion in instrucciones:
        if instruccion is not None:
            instruccion.ejecutar(env)
except Exception as e:
    print(f"Error inesperado: {e}")


print('TABLA DE SIMBOLOS:')
print(Enviroment.serializarTodosSimbolos())
print('TABLA DE ERRORES:')
print(TablaErrores.serializarTBErrores())

ast = AST(instrucciones)
ast.getAST()



Enviroment.cleanEnviroments()
TablaErrores.cleanTablaErrores()