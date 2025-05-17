from datetime import datetime

def generar_ticket(cliente, items_compra, total):
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