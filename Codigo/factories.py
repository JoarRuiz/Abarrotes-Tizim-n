from cliente import Cliente
from articulo import Articulo

class ClienteFactory:
    @staticmethod
    def from_row(row: tuple) -> Cliente:
        """Fila SQL → objeto Cliente."""
        return Cliente(*row)
