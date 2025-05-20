#Objetos de la clase cliente
class Cliente:
    def __init__(self, identificador, nombre, apellido, calle, numero, colonia, cp, ciudad, estado, telefono):
        self.identificador = identificador
        self.nombre = nombre
        self.apellido = apellido
        self.calle = calle
        self.numero = numero
        self.colonia = colonia
        self.cp = cp
        self.ciudad = ciudad
        self.estado = estado
        self.telefono = telefono

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.telefono})"
