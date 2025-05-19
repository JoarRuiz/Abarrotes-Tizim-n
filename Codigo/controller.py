from cliente import Cliente
from articulo import Articulo
from factory import ClienteFactory, ArticuloFactory
from ticket import generar_ticket
from datetime import datetime
from db import DatabaseManager

class SistemaAbarrotesController:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db = DatabaseManager()
        return cls._instance

    # ---- Clientes ----
    def registrar_cliente(self, datos_cliente):
        """Registra un nuevo cliente manteniendo el estilo Factory."""
        try:
            cliente = Cliente(*datos_cliente)
            cur = self.db.cursor()
            cur.execute("""INSERT INTO clientes VALUES (?,?,?,?,?,?,?,?,?,?)""", datos_cliente)
            self.db.commit()
            return "Cliente registrado"
        except Exception as e:
            raise ValueError(f"Error al registrar: {str(e)}")

    def obtener_clientes(self):
        """Obtiene todos los clientes usando el patrón Factory existente."""
        cur = self.db.cursor()
        cur.execute("SELECT * FROM clientes")
        return [ClienteFactory.from_row(row) for row in cur.fetchall()]

    # ---- Artículos ----
    def registrar_articulo(self, datos_articulo):
        try:
            articulo = Articulo(*datos_articulo)
            cur = self.db.cursor()
            cur.execute("""INSERT INTO articulos VALUES (?,?,?,?,?)""", datos_articulo)
            self.db.commit()
            return "Artículo registrado"
        except ValueError as e:
            raise ValueError(f"Dato inválido: {str(e)}")

    def obtener_articulos(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM articulos")
        return [ArticuloFactory.from_row(row) for row in cur.fetchall()]

    def obtener_articulos_disponibles(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM articulos WHERE existencia > 0")
        return [ArticuloFactory.from_row(row) for row in cur.fetchall()]

    # ---- Compras ----
    def procesar_compra(self, cliente_id, items):
        try:
            cliente = self._obtener_cliente_por_id(cliente_id)
            articulos = self._validar_items_compra(items)
            total = sum(a.precio_publico * cant for a, cant in articulos)
            
            self._actualizar_inventario(articulos)
            return generar_ticket(cliente, articulos, total)
        except Exception as e:
            raise ValueError(f"Error en compra: {str(e)}")

    # ---- Métodos privados ----
    def _obtener_cliente_por_id(self, id):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM clientes WHERE id=?", (id,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Cliente no encontrado")
        return ClienteFactory.from_row(row)

    def _obtener_articulo_por_id(self, id):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM articulos WHERE id=?", (id,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Artículo no encontrado")
        return ArticuloFactory.from_row(row)

    def _validar_items_compra(self, items):
        articulos_validos = []
        for art_id, cant in items:
            articulo = self._obtener_articulo_por_id(art_id)
            if articulo.existencia < cant:
                raise ValueError(f"Stock insuficiente: {articulo.nombre}")
            articulos_validos.append((articulo, cant))
        return articulos_validos

    def _actualizar_inventario(self, articulos):
        cur = self.db.cursor()
        try:
            for articulo, cant in articulos:
                cur.execute("""
                    UPDATE articulos 
                    SET existencia = existencia - ? 
                    WHERE id = ?
                """, (cant, articulo.identificador))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error al actualizar inventario: {str(e)}")