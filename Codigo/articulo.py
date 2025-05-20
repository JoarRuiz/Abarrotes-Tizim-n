#Objetos de la clase articulo
class Articulo:
    def __init__(self, identificador, nombre, precio_publico, precio_proveedor, existencia):
        self.identificador = identificador
        self.nombre = nombre
        self.precio_publico = precio_publico
        self.precio_proveedor = precio_proveedor
        self.existencia = existencia

    def __str__(self):
        return f"{self.nombre} - ${self.precio_publico} (Existencia: {self.existencia})"
