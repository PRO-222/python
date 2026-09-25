from model import ModeloTraduccion

class ControladorTraduccion:
    def __init__(self):
        self.modelo = ModeloTraduccion()

    def cargar_palabra (self, esp, ing):
        self.modelo.agregar_palabra(esp, ing)

    def buscar_palabra(self, palabra):
        return self.modelo.buscar_palabra(palabra)

    def traducir(self, palabra):
        resultado = self.modelo.buscar_palabra(palabra)
        if resultado != None:
            return  resultado

        return None