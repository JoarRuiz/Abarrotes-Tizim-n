from datetime import datetime

#Objetos de la compra
class Compra:
    def __init__(self, cliente, articulos, total):
        self.cliente = cliente
        self.articulos = articulos
        self.total = total
        self.fecha = datetime.now()

