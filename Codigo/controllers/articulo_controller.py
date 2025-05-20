from articulo import Articulo
from factory import ArticuloFactory
from db import DatabaseManager

class ArticuloController:
    def __init__(self, db_manager):
        self.db = db_manager

    #Registro de un nuevo articulo en el sistema.
    def registrar_articulo(self, datos_articulo):
        try:
            articulo = Articulo(*datos_articulo)
            cur = self.db.cursor()
            cur.execute("""INSERT INTO articulos VALUES (?,?,?,?,?)""", datos_articulo)
            self.db.commit()
            return "Artículo registrado"
        except ValueError as e:
            raise ValueError(f"Dato inválido: {str(e)}")

    #Obtencion de la lista de los artículos
    def obtener_articulos(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM articulos")
        return [ArticuloFactory.from_row(row) for row in cur.fetchall()]

    #Obtencion de los articulos con los que se tiene stock
    def obtener_articulos_disponibles(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM articulos WHERE existencia > 0")
        return [ArticuloFactory.from_row(row) for row in cur.fetchall()]

    #Obtencion del articulo por su id
    def obtener_articulo_por_id(self, id):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM articulos WHERE id=?", (id,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Artículo no encontrado")
        return ArticuloFactory.from_row(row)

    #Actualiza el stock de un artículo en la db
    def actualizar_inventario(self, articulo_id, cantidad):
        cur = self.db.cursor()
        try:
            cur.execute("""
                UPDATE articulos 
                SET existencia = existencia + ? 
                WHERE id = ?
            """, (cantidad, articulo_id))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error al actualizar inventario: {str(e)}")