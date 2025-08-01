from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from analizadores.parser import parser
from analizadores.lexer import lexer
from interprete.otros.enviroment import Enviroment
from interprete.otros.ast import AST
from interprete.otros.consola import Consola
from interprete.otros.errores import TablaErrores, Error
from interprete.instrucciones.iWhile import While
from interprete.instrucciones.iDoWhile import DoWhile
from interprete.instrucciones.iSwitch import Switch
from interprete.instrucciones.iFor import For
from interprete.otros.reporteVectores import ReporteVectores 

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origin": "*"}})

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/datas", methods=['POST'])
def datas():
    if request.method == 'POST':
        data = request.data.decode('utf-8')

        While.reset_contador()
        DoWhile.reset_contador() 
        Enviroment.cleanEnviroments()
        Switch.reset_contador()
        For.reset_contador() 
        TablaErrores.cleanTablaErrores()
        ReporteVectores.cleanReporteVectores()  # ← Solo agregar esta línea
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

        ast = AST(instrucciones)
        ast.getAST()    

        # Guardar la tabla de simbolos antes de limpiar el Enviroment
        # Para que no se dupliquen las declaraciones, asignaciones, etc.
        # Y esto es lo que se va a enviar
        env_serializado = Enviroment.serializarTodosSimbolos()
        vectores_serializados = ReporteVectores.serializarVectores()  # ← Solo agregar esta línea

        # ← Modificar solo esta parte - agregar ListVector
        tuple = {'ListConsole': Consola.getConsola(), 
                 'ListError': TablaErrores.serializarTBErrores(), 
                 'ListSymbol': env_serializado,
                 'ListVector': vectores_serializados}  # ← Solo agregar esta línea

        Enviroment.cleanEnviroments()
        TablaErrores.cleanTablaErrores()
        Consola.cleanConsola()
        ReporteVectores.cleanReporteVectores()  # ← Solo agregar esta línea
        
        return jsonify(tuple) 
    
@app.route('/ast')
def ast():
    image_path = 'AST.png'
    return send_file(image_path, mimetype='image/png')

if __name__=='__main__':
    app.run(debug = True, port = 5000)