from interprete.otros.tipos import TipoSimbolo
from interprete.otros.symbol import Symbol

class TablaSimbolos:
    def __init__(self):
        self.ts:TablaSimbolos = {}
        
    def instertarSimbolo(self, id:str, simbolo:Symbol):
        self.ts[id] = simbolo
    
    def buscarSimbolo(self, id:str):
        return self.ts.get(id)

    def getSimbolo(self, id:str) -> Symbol:
        return self.ts.get(id)
    
    def getTS(self):
        return self.ts.values()