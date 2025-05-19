from abc import ABC, abstractmethod
from datetime import datetime

# Interfaz Strategy
class TicketStrategy(ABC):
    @abstractmethod
    def generar(self, cliente, items_compra, total) -> str:
        pass

# Estrategia concreta 1: Ticket básico
class TicketBasicoStrategy(TicketStrategy):
    def generar(self, cliente, items_compra, total) -> str:
        ticket = f"""
=== TICKET DE COMPRA ===
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Cliente: {cliente.nombre} {cliente.apellido}
-------------------------"""
        
        for articulo, cantidad in items_compra:
            subtotal = articulo.precio_publico * cantidad
            ticket += f"""
Producto: {articulo.nombre}
Cantidad: {cantidad}
Precio unitario: ${articulo.precio_publico:.2f}
Subtotal: ${subtotal:.2f}
-------------------------"""
        
        ticket += f"""
TOTAL: ${total:.2f}
========================="""
        return ticket

# Estrategia concreta 2: Ticket detallado
class TicketDetalladoStrategy(TicketStrategy):
    def generar(self, cliente, items_compra, total) -> str:
        ticket = f"""
=== TICKET DETALLADO ===
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Cliente: {cliente.nombre} {cliente.apellido}
ID Cliente: {cliente.identificador}
Teléfono: {cliente.telefono}
-------------------------"""
        
        for articulo, cantidad in items_compra:
            subtotal = articulo.precio_publico * cantidad
            margen = articulo.precio_publico - articulo.precio_proveedor
            ticket += f"""
Producto: {articulo.nombre} (ID: {articulo.identificador})
Cantidad: {cantidad}
P. Unitario: ${articulo.precio_publico:.2f}
Margen: ${margen:.2f}
Subtotal: ${subtotal:.2f}
-------------------------"""
        
        ticket += f"""
TOTAL: ${total:.2f}
Artículos: {len(items_compra)}
========================="""
        return ticket

# Contexto (usa Singleton)
class TicketGenerator:
    _instance = None
    _strategy = TicketBasicoStrategy()  # Estrategia por defecto

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_strategy(self, strategy: TicketStrategy):
        self._strategy = strategy

    def generar_ticket(self, cliente, items_compra, total):
        return self._strategy.generar(cliente, items_compra, total)

# Función original (para compatibilidad)
def generar_ticket(cliente, items_compra, total):
    return TicketGenerator().generar_ticket(cliente, items_compra, total)