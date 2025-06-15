from interprete.otros.ast import *
from interprete.otros.tipos import TipoDato
from .instruccion import Instruccion
from interprete.otros.enviroment import Enviroment
from interprete.otros.errores import Error, TablaErrores

class While(Instruccion):
    def __init__(self, text_val:str, condicion, instrucciones, linea, columna):
        super().__init__(text_val, linea, columna)
        self.condicion = condicion
        self.instrucciones = instrucciones
        
        # Calcular nivel de anidamiento basado en el entorno
        self.nivel_anidamiento = self._calcular_nivel_while()
        self.nombre_while = f"while{self.nivel_anidamiento}"
    
    def _calcular_nivel_while(self):
        # Contar cuántos while hay en la cadena de llamadas
        import inspect
        frame = inspect.currentframe()
        contador = 0
        
        try:
            while frame:
                if frame.f_code.co_name == 'ejecutar' and 'While' in str(frame.f_locals.get('self', '')):
                    contador += 1
                frame = frame.f_back
        finally:
            del frame
        
        return contador + 1
    
    def ejecutar(self, env:Enviroment):
        # Crear nuevo entorno para el while
        entorno_while = Enviroment(env, self.nombre_while)
        
        while True:
            # Evaluar condición
            resultado_condicion = self.condicion.ejecutar(entorno_while)
            
            # Validar que la condición sea booleana
            if resultado_condicion.tipo != TipoDato.BOOLEAN:
                err = Error(tipo='Semántico', linea=self.linea, columna=self.columna, 
                          descripcion=f'La condición del while debe ser de tipo boolean')
                TablaErrores.addError(err)
                break
            
            # Si la condición es falsa, salir del ciclo
            if not resultado_condicion.valor:
                break
            
            # Ejecutar instrucciones del while
            for instruccion in self.instrucciones:
                resultado = instruccion.ejecutar(entorno_while)
                
                # Aquí puedes manejar break y continue en el futuro
                # if isinstance(resultado, Break):
                #     return resultado
                # if isinstance(resultado, Continue):
                #     break
        
        return self
    
    def recorrerArbol(self, raiz:Nodo):
        id = AST.generarId()
        hijo = Nodo(id=id, valor=f'WHILE({self.nombre_while})', hijos=[])
        raiz.addHijo(hijo)
        
        # Agregar nodo de condición
        id = AST.generarId()
        nodo_condicion = Nodo(id=id, valor='CONDICION', hijos=[])
        hijo.addHijo(nodo_condicion)
        self.condicion.recorrerArbol(nodo_condicion)
        
        # Agregar nodo de instrucciones
        id = AST.generarId()
        nodo_instrucciones = Nodo(id=id, valor='INSTRUCCIONES', hijos=[])
        hijo.addHijo(nodo_instrucciones)
        
        for instruccion in self.instrucciones:
            instruccion.recorrerArbol(nodo_instrucciones)
    
    @classmethod
    def reset_contador(cls):
        """Método para resetear el contador al inicio de cada análisis"""
        cls.contador_while = 0