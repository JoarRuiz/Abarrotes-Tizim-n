# factory para las listas de datos
from cliente import Cliente
from articulo import Articulo

class ClienteFactory:
    @staticmethod
    def from_row(row: tuple) -> Cliente:
        """Fila SQL → objeto Cliente."""
        return Cliente(*row)

class ArticuloFactory:
    @staticmethod
    def from_row(row: tuple) -> Articulo:
        return Articulo(*row)
