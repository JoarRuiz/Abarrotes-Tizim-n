
from cliente import Cliente
from articulo import Articulo
#Factory para la lista de datos de cliente
class ClienteFactory:
    @staticmethod
    def from_row(row: tuple) -> Cliente:
        """Fila SQL → objeto Cliente."""
        return Cliente(*row)

#Factory para la lista de datos de Articulos
class ArticuloFactory:
    @staticmethod
    def from_row(row: tuple) -> Articulo:
        return Articulo(*row)
