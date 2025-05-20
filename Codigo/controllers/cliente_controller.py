from cliente import Cliente
from factory import ClienteFactory
from db import DatabaseManager

class ClienteController:
    def __init__(self, db_manager):
        self.db = db_manager

    #Registro de un nuevo cliente
    def registrar_cliente(self, datos_cliente):
        try:
            cliente = Cliente(*datos_cliente)
            cur = self.db.cursor()
            cur.execute("""INSERT INTO clientes VALUES (?,?,?,?,?,?,?,?,?,?)""", datos_cliente)
            self.db.commit()
            return "Cliente registrado"
        except Exception as e:
            raise ValueError(f"Error al registrar: {str(e)}")

    #Obtencion de los clientes 
    def obtener_clientes(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM clientes")
        return [ClienteFactory.from_row(row) for row in cur.fetchall()]

    #Obtencion de un cliente por su id
    def obtener_cliente_por_id(self, id):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM clientes WHERE id=?", (id,))
        row = cur.fetchone()
        if not row:
            raise ValueError("Cliente no encontrado")
        return ClienteFactory.from_row(row)