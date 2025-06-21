#Genera una lista que retornaba los print de consola
class Consola:  #prints
    consola:str = []
    def __init__(self):
        pass
    
    @classmethod
    def serializar(cls):
        return {
            'consola': cls.consola 
        }

    @classmethod
    def addConsola(cls, datos:str):
        cls.consola.append(str(datos))
    
    @classmethod
    def getConsola(cls):
        return cls.consola
    
    @classmethod
    def cleanConsola(cls):
        cls.consola = []