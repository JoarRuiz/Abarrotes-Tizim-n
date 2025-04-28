import tkinter as tk
from tkinter import ttk, messagebox
from cliente import Cliente
from db import DatabaseManager   
from factories import ClienteFactory, ArticuloFactory


# instancia única de singleton
db = DatabaseManager()

#  Eliminar ventanas inecesarias
def Quitar_ventana():
    for w in root.winfo_children():
        w.destroy()


# Menu de administrador
def mostrar_menu():
    Quitar_ventana()
    ttk.Label(root, text="Menú Principal", font=("Arial", 16)).pack(pady=20)
    ttk.Button(root, text="Registrar Cliente",   command=registrar_cliente).pack(pady=10)
    ttk.Button(root, text="Registrar Artículo",  command=registrar_cliente).pack(pady=10)
    ttk.Button(root, text="Realizar Compra",     command=registrar_cliente).pack(pady=10)
    ttk.Button(root, text="Salir",               command=root.destroy).pack(pady=10)


# Registro de clientes
def registrar_cliente():
    Quitar_ventana()
    ttk.Label(root, text="Registro de Cliente", font=("Arial", 14)).pack(pady=10)

    campos = ["ID", "Nombre", "Apellido", "Calle", "Número",
              "Colonia", "CP", "Ciudad", "Estado", "Teléfono"]
    entradas = {}
    for c in campos:
        ttk.Label(root, text=c).pack()
        e = ttk.Entry(root)
        e.pack()
        entradas[c] = e

    def guardar():
        datos = [entradas[c].get() for c in campos]
        if not all(datos):
            messagebox.showerror("Error", "Por favor llena todos los campos")
            return
        cliente = Cliente(*datos)
        cur = db.cursor()
        cur.execute("""INSERT INTO clientes VALUES (?,?,?,?,?,?,?,?,?,?)""",
                    (cliente.identificador, cliente.nombre, cliente.apellido,
                     cliente.calle, cliente.numero, cliente.colonia,
                     cliente.cp, cliente.ciudad, cliente.estado, cliente.telefono))
        db.commit()
        messagebox.showinfo("Éxito", "Cliente registrado")
        mostrar_clientes()

    f = ttk.Frame(root); f.pack(pady=10)
    ttk.Button(f, text="Guardar Cliente", command=guardar)      .grid(row=0, column=0, padx=10)
    ttk.Button(f, text="Cancelar",        command=mostrar_menu).grid(row=0, column=1, padx=10)


# Tabla para mostrar los clientes

def mostrar_clientes():
    Quitar_ventana()
    ttk.Label(root, text="Clientes Registrados", font=("Arial", 14)).pack(pady=10)

    tree = ttk.Treeview(root, columns=("ID","Nombre","Apellido","Ciudad"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(pady=10)

    cur = db.cursor()
    cur.execute("SELECT * FROM clientes")
    for row in cur.fetchall():
        c = ClienteFactory.from_row(row)
        tree.insert("", tk.END, values=(c.identificador, c.nombre, c.apellido, c.ciudad))

    ttk.Button(root, text="Volver al Menú", command=mostrar_menu).pack(pady=10)


root = tk.Tk()
root.title("Abarrotes Tizimín")
root.geometry("700x500")
mostrar_menu()
root.mainloop()
