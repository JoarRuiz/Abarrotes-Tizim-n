from ticket import TicketGenerator
from db import DatabaseManager

class CompraController:
    def __init__(self, db_manager, cliente_controller, articulo_controller):
        self.db = db_manager
        self.cliente_controller = cliente_controller
        self.articulo_controller = articulo_controller

    #Procesa la compra y genera el ticket
    def procesar_compra(self, cliente_id, items):
        try:
            cliente = self.cliente_controller.obtener_cliente_por_id(cliente_id)
            articulos = self._validar_items_compra(items)
            total = sum(a.precio_publico * cant for a, cant in articulos)
            
            self._actualizar_inventario(articulos)
            
            ticket = TicketGenerator().generar_ticket(cliente, articulos, total)
            return ticket
        except Exception as e:
            raise ValueError(f"Error en compra: {str(e)}")

    #Revisa que los articulos seleccionados concuerden con el stock existente
    def _validar_items_compra(self, items):
        articulos_validos = []
        for art_id, cant in items:
            articulo = self.articulo_controller.obtener_articulo_por_id(art_id)
            if articulo.existencia < cant:
                raise ValueError(f"Stock insuficiente: {articulo.nombre}")
            articulos_validos.append((articulo, cant))
        return articulos_validos

    #Actualiza el stock de los productos seleccionados después de una compra
    def _actualizar_inventario(self, articulos):
        cur = self.db.cursor()
        try:
            for articulo, cant in articulos:
                self.articulo_controller.actualizar_inventario(articulo.identificador, -cant)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error al actualizar inventario: {str(e)}")