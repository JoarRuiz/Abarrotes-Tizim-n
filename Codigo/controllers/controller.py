from db import DatabaseManager
from controllers.cliente_controller import ClienteController
from controllers.articulo_controller import ArticuloController
from controllers.compra_controller import CompraController

class SistemaAbarrotesController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db = DatabaseManager()
            cls._instance.cliente = ClienteController(cls._instance.db)
            cls._instance.articulo = ArticuloController(cls._instance.db)
            cls._instance.compra = CompraController(
                cls._instance.db,
                cls._instance.cliente,
                cls._instance.articulo
            )
        return cls._instance

    # Métodos para mantener la compativilidad con el main
    def registrar_cliente(self, datos_cliente):
        return self.cliente.registrar_cliente(datos_cliente)

    def obtener_clientes(self):
        return self.cliente.obtener_clientes()

    def registrar_articulo(self, datos_articulo):
        return self.articulo.registrar_articulo(datos_articulo)

    def obtener_articulos(self):
        return self.articulo.obtener_articulos()

    def obtener_articulos_disponibles(self):
        return self.articulo.obtener_articulos_disponibles()

    def procesar_compra(self, cliente_id, items):
        return self.compra.procesar_compra(cliente_id, items)

    def _obtener_cliente_por_id(self, id):
        return self.cliente.obtener_cliente_por_id(id)

    def _obtener_articulo_por_id(self, id):
        return self.articulo.obtener_articulo_por_id(id)