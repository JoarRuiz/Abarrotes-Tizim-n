import sqlite3
from pathlib import Path

class DatabaseManager:
    """Singleton para manejar UNA sola conexión SQLite."""
    _instance = None

    def __new__(cls, db_name: str = "abarrotes.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init(db_name)
        return cls._instance

    # Metodo de la instancia de singleton
    def _init(self, db_name: str):
        self._path = Path(db_name)
        self.conn = sqlite3.connect(self._path)
        self._crear_tablas()

    def cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    # Creacion de tablas
    def _crear_tablas(self):
        cur = self.cursor()
        cur.execute("""
          CREATE TABLE IF NOT EXISTS clientes(
              id TEXT PRIMARY KEY,
              nombre TEXT, apellido TEXT,
              calle TEXT, numero TEXT, colonia TEXT,
              cp TEXT, ciudad TEXT, estado TEXT, telefono TEXT)
        """)
        cur.execute("""
          CREATE TABLE IF NOT EXISTS articulos(
              id TEXT PRIMARY KEY,
              nombre TEXT,
              precio_publico REAL,
              precio_proveedor REAL,
              existencia INTEGER)
        """)
        self.commit()
