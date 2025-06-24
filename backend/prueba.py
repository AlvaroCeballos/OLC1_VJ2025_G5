from analizadores.parser import parser
from analizadores.lexer import lexer
from interprete.otros.enviroment import Enviroment
from interprete.otros.ast import AST
from interprete.otros.consola import Consola
from interprete.otros.errores import TablaErrores, Error
from interprete.instrucciones.iWhile import While
from interprete.instrucciones.iDoWhile import DoWhile

# Setup
f = open('backend/pruebaVectores.txt', 'r', encoding='utf-8')
data = f.read()

# Reset
While.reset_contador()
DoWhile.reset_contador() 
Enviroment.cleanEnviroments()
TablaErrores.cleanTablaErrores()
Consola.cleanConsola()
lexer.lineno = 1

# Parse y ejecución
try:
    instrucciones = parser.parse(data, lexer=lexer) or []
    env = Enviroment(ent_anterior=None, ambito='Global')
    
    for instruccion in instrucciones:
        if instruccion:
            try:
                instruccion.ejecutar(env)
            except Exception as e:
                TablaErrores.addError(Error('Ejecución', 0, 0, str(e)))
                
except Exception as e:
    TablaErrores.addError(Error('Fatal', 0, 0, str(e)))

# Resultados
for linea in Consola.getConsola():
    print(f">>> {linea}")

print('\nTABLA DE SÍMBOLOS:')
print(Enviroment.serializarTodosSimbolos())

print('\nTABLA DE ERRORES:')
print(TablaErrores.serializarTBErrores())

# Cleanup
try:
    ast = AST(instrucciones)
    ast.getAST()
except:
    pass

Enviroment.cleanEnviroments()
TablaErrores.cleanTablaErrores()