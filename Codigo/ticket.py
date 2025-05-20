from abc import ABC, abstractmethod
from datetime import datetime

# Interfaz  para el patron de diseño strategy
class TicketStrategy(ABC):
    @abstractmethod
    def generar(self, cliente, items_compra, total) -> str:
        pass

# Estrategia 1: ticket basico
class TicketBasicoStrategy(TicketStrategy):
    def generar(self, cliente, items_compra, total) -> str:
        ticket = f"""
======= Ticket de compra =======
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
Total: ${total:.2f}
========================="""
        return ticket

# Estrategia 2: Ticket detallado
class TicketDetalladoStrategy(TicketStrategy):
    def generar(self, cliente, items_compra, total) -> str:
        ticket = f"""
======= TICKET ========
Fecha de compra: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Cliente: {cliente.nombre} {cliente.apellido}
ID: {cliente.identificador}
Teléfono: {cliente.telefono}
-------------------------"""
        
        for articulo, cantidad in items_compra:
            subtotal = articulo.precio_publico * cantidad
            margen = articulo.precio_publico - articulo.precio_proveedor
            ticket += f"""
Producto:(ID: {articulo.identificador}) {articulo.nombre} 
Cantidad: {cantidad}
Precio Unitario: ${articulo.precio_publico:.2f}
Subtotal: ${subtotal:.2f}
-------------------------"""
        
        ticket += f"""
Cantidad total de artículos: {len(items_compra)}
Total: ${total:.2f}

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