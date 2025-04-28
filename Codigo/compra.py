from datetime import datetime

class Compra:
    def __init__(self, cliente, articulo, cantidad):
        self.cliente = cliente
        self.articulo = articulo
        self.cantidad = cantidad
        self.fecha = datetime.now()

    def calcular_total(self):
        return self.cantidad * self.articulo.precio_publico

    def generar_ticket(self):
        ticket = f"""
        Ticket de compra /n

        Fecha: {self.fecha.strftime("%Y-%m-%d %H:%M:%S")}
        Cliente: {self.cliente.nombre} {self.cliente.apellido}

        Artículo: {self.articulo.nombre}
        Cantidad: {self.cantidad}
        Precio unitario: ${self.articulo.precio_publico:.2f}
        Total: ${self.calcular_total():.2f}
        /n
        """
        return ticket
