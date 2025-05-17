import tkinter as tk
from tkinter import ttk, messagebox
from cliente import Cliente
from articulo import Articulo
from db import DatabaseManager
from factory import ClienteFactory, ArticuloFactory
from ticket import generar_ticket
from datetime import datetime

'''
Instancia de singleton para la base de datos

'''
db = DatabaseManager()

'''Limpieza de interfaces'''
def limpiar_ventana():
    for w in root.winfo_children():
        w.destroy()
'''

Menu del adminsitrador

'''
def mostrar_menu():
    limpiar_ventana()
    root.geometry("400x300")
    ttk.Label(root, text="Menú Principal", font=("Arial", 16)).pack(pady=20)
    ttk.Button(root, text="Registrar Cliente", command=registrar_cliente, width=20).pack(pady=10)
    ttk.Button(root, text="Registrar Artículo", command=registrar_articulo, width=20).pack(pady=10)
    ttk.Button(root, text="Realizar Compra", command=realizar_compra, width=20).pack(pady=10)
    ttk.Button(root, text="Salir", command=root.destroy, width=20).pack(pady=10)

'''

Registro de Clientes

'''
def registrar_cliente():
    limpiar_ventana()
    root.geometry("500x550")
    
    frame_principal = ttk.Frame(root)
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    ttk.Label(frame_principal, text="Registro de Cliente", font=("Arial", 14)).pack(pady=10)

    campos = ["ID", "Nombre", "Apellido", "Calle", "Número", 
              "Colonia", "CP", "Ciudad", "Estado", "Teléfono"]
    entradas = {}
    for c in campos:
        ttk.Label(frame_principal, text=c).pack()
        e = ttk.Entry(frame_principal)
        e.pack()
        entradas[c] = e

    def guardar():
        datos = [entradas[c].get() for c in campos]
        if not all(datos):
            messagebox.showerror("Error", "Por favor llena todos los campos")
            return
        
        try:
            cliente = Cliente(*datos)
            cur = db.cursor()
            cur.execute("""INSERT INTO clientes VALUES (?,?,?,?,?,?,?,?,?,?)""",
                        (cliente.identificador, cliente.nombre, cliente.apellido,
                         cliente.calle, cliente.numero, cliente.colonia,
                         cliente.cp, cliente.ciudad, cliente.estado, cliente.telefono))
            db.commit()
            messagebox.showinfo("Éxito", "Cliente registrado")
            mostrar_clientes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {str(e)}")

    f = ttk.Frame(frame_principal)
    f.pack(pady=15)
    ttk.Button(f, text="Guardar Cliente", command=guardar).grid(row=0, column=0, padx=10)
    ttk.Button(f, text="Cancelar", command=mostrar_menu).grid(row=0, column=1, padx=10)
    ttk.Button(f, text="Ver Lista de Clientes", command=mostrar_clientes).grid(row=0, column=2, padx=10)

'''
Tabla de clientes 

'''
def mostrar_clientes():
    limpiar_ventana()
    root.geometry("1000x500")
    
    frame_principal = ttk.Frame(root)
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    ttk.Label(frame_principal, text="Clientes Registrados", font=("Arial", 14)).pack(pady=10)

    # Configurar Treeview
    frame_tabla = ttk.Frame(frame_principal)
    frame_tabla.pack(fill=tk.BOTH, expand=True)

    columnas = [
        ("ID", 80),
        ("Nombre", 120),
        ("Apellido", 120),
        ("Teléfono", 100),
        ("Calle", 150),
        ("Número", 70),
        ("Colonia", 150),
        ("CP", 70),
        ("Ciudad", 120),
        ("Estado", 100)
    ]

    tree = ttk.Treeview(frame_tabla, columns=[col[0] for col in columnas], show="headings", height=15)

    for col, width in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor="w")

    tree.pack(side="left", fill=tk.BOTH, expand=True)

    # Campo de para los datos del cliente 
    cur = db.cursor()
    cur.execute("SELECT * FROM clientes")
    for row in cur.fetchall():
        c = ClienteFactory.from_row(row)
        tree.insert("", tk.END, values=(
            c.identificador,
            c.nombre,
            c.apellido,
            c.telefono,
            c.calle,
            c.numero,
            c.colonia,
            c.cp,
            c.ciudad,
            c.estado
        ))

    def editar_cliente():
        item = tree.focus()
        if not item:
            messagebox.showerror("Error", "Selecciona un cliente")
            return
        id_sel = tree.item(item)["values"][0]

        top = tk.Toplevel(root)
        top.title("Editar Cliente")
        top.geometry("300x400")
        
        cur.execute("SELECT * FROM clientes WHERE id=?", (id_sel,))
        cliente_data = cur.fetchone()
        cliente = ClienteFactory.from_row(cliente_data)

        # Mostrar información no editable
        ttk.Label(top, text="ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        ttk.Label(top, text=cliente.identificador).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(top, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        ttk.Label(top, text=cliente.nombre).grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(top, text="Apellido:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        ttk.Label(top, text=cliente.apellido).grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Campos editables
        campos_editables = [
            ("Calle", cliente.calle),
            ("Número", cliente.numero),
            ("Colonia", cliente.colonia),
            ("CP", cliente.cp),
            ("Ciudad", cliente.ciudad),
            ("Estado", cliente.estado),
            ("Teléfono", cliente.telefono)
        ]

        entries = {}
        for i, (campo, valor) in enumerate(campos_editables, start=3):
            ttk.Label(top, text=f"{campo}:").grid(row=i, column=0, padx=10, pady=5, sticky="e")
            e = ttk.Entry(top)
            e.insert(0, valor)
            e.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entries[campo] = e

        def actualizar():
            try:
                cur.execute("""
                    UPDATE clientes SET
                        calle=?, numero=?, colonia=?,
                        cp=?, ciudad=?, estado=?, telefono=?
                    WHERE id=?
                """, (
                    entries["Calle"].get(),
                    entries["Número"].get(),
                    entries["Colonia"].get(),
                    entries["CP"].get(),
                    entries["Ciudad"].get(),
                    entries["Estado"].get(),
                    entries["Teléfono"].get(),
                    id_sel
                ))
                db.commit()
                messagebox.showinfo("Éxito", "Cliente actualizado")
                top.destroy()
                mostrar_clientes()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {e}")

        def eliminar():
            if messagebox.askyesno("Confirmar", "¿Eliminar este cliente permanentemente?"):
                try:
                    cur.execute("SELECT COUNT(*) FROM compras WHERE cliente_id=?", (id_sel,))
                    if cur.fetchone()[0] > 0:
                        messagebox.showwarning("Error", "No se puede eliminar, el cliente tiene compras registradas")
                        return
                    
                    cur.execute("DELETE FROM clientes WHERE id=?", (id_sel,))
                    db.commit()
                    messagebox.showinfo("Éxito", "Cliente eliminado")
                    top.destroy()
                    mostrar_clientes()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar: {e}")

        btn_frame = ttk.Frame(top)
        btn_frame.grid(row=len(campos_editables)+4, column=0, columnspan=2, pady=15)
        ttk.Button(btn_frame, text="Guardar", command=actualizar).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Eliminar", command=eliminar).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=top.destroy).pack(side="left", padx=10)

    btn_frame = ttk.Frame(frame_principal)
    btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text="Editar Cliente", command=editar_cliente).pack(side="left", padx=10)
    ttk.Button(btn_frame, text="Volver al Menú", command=mostrar_menu).pack(side="left", padx=10)

'''
registro de los articulos 

'''
def registrar_articulo():
    limpiar_ventana()
    root.geometry("500x400")
    
    frame_principal = ttk.Frame(root)
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    ttk.Label(frame_principal, text="Registro de Artículo", font=("Arial", 14)).pack(pady=10)

    campos = ["ID", "Nombre", "Precio Público", "Precio Proveedor", "Existencia"]
    entradas = {}
    for c in campos:
        ttk.Label(frame_principal, text=c).pack()
        e = ttk.Entry(frame_principal)
        e.pack()
        entradas[c] = e

    def guardar():
        try:
            datos = [entradas[c].get() for c in campos]
            if not all(datos):
                raise ValueError("Todos los campos son obligatorios")
            
            art = Articulo(
                datos[0], 
                datos[1],
                float(datos[2]), 
                float(datos[3]), 
                int(datos[4])
            )
            
            cur = db.cursor()
            cur.execute("""INSERT INTO articulos VALUES (?,?,?,?,?)""",
                        (art.identificador, art.nombre, art.precio_publico,
                         art.precio_proveedor, art.existencia))
            db.commit()
            messagebox.showinfo("Éxito", "Artículo registrado")
            mostrar_articulos()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Dato inválido: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {str(e)}")

    f = ttk.Frame(frame_principal)
    f.pack(pady=15)
    ttk.Button(f, text="Guardar Artículo", command=guardar).grid(row=0, column=0, padx=10)
    ttk.Button(f, text="Cancelar", command=mostrar_menu).grid(row=0, column=1, padx=10)
    ttk.Button(f, text="Ver Lista de Artículos", command=mostrar_articulos).grid(row=0, column=2, padx=10)

'''

Tabla con los datos de los articulos

'''
def mostrar_articulos():
    limpiar_ventana()
    root.geometry("700x500")
    
    frame_principal = ttk.Frame(root)
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    ttk.Label(frame_principal, text="Artículos Registrados", font=("Arial", 14)).pack(pady=10)

    # Configurar Treeview
    frame_tabla = ttk.Frame(frame_principal)
    frame_tabla.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame_tabla, columns=("ID","Nombre","Precio","Existencia"), show="headings", height=15)

    # Configurar columnas
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Precio", text="Precio Público")
    tree.heading("Existencia", text="Existencia")

    tree.column("ID", width=100, anchor="w")
    tree.column("Nombre", width=250, anchor="w")
    tree.column("Precio", width=150, anchor="e")
    tree.column("Existencia", width=100, anchor="e")

    tree.pack(side="left", fill=tk.BOTH, expand=True)

    # Llenar datos
    cur = db.cursor()
    cur.execute("SELECT * FROM articulos")
    for row in cur.fetchall():
        a = ArticuloFactory.from_row(row)
        tree.insert("", tk.END, values=(
            a.identificador, 
            a.nombre, 
            f"${a.precio_publico:.2f}", 
            a.existencia
        ))

    def editar_articulo():
        item = tree.focus()
        if not item:
            messagebox.showerror("Error", "Selecciona un artículo")
            return
        id_sel = tree.item(item)["values"][0]

        top = tk.Toplevel(root)
        top.title("Editar Artículo")
        top.geometry("300x300")
        
        cur.execute("SELECT * FROM articulos WHERE id=?", (id_sel,))
        articulo_data = cur.fetchone()
        articulo = ArticuloFactory.from_row(articulo_data)

        # Mostrar información no editable
        ttk.Label(top, text="ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        ttk.Label(top, text=articulo.identificador).grid(row=0, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(top, text="Nombre:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        ttk.Label(top, text=articulo.nombre).grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Campos editables
        ttk.Label(top, text="Precio Público:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        e_precio = ttk.Entry(top)
        e_precio.insert(0, articulo.precio_publico)
        e_precio.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(top, text="Precio Proveedor:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        e_precio_prov = ttk.Entry(top)
        e_precio_prov.insert(0, articulo.precio_proveedor)
        e_precio_prov.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(top, text="Existencia:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        e_existencia = ttk.Entry(top)
        e_existencia.insert(0, articulo.existencia)
        e_existencia.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        def actualizar():
            try:
                nuevo_precio = float(e_precio.get())
                nuevo_precio_prov = float(e_precio_prov.get())
                nueva_existencia = int(e_existencia.get())
                
                if nuevo_precio <= 0 or nuevo_precio_prov <= 0 or nueva_existencia < 0:
                    raise ValueError("Valores deben ser positivos")
                    
                cur.execute("""
                    UPDATE articulos SET
                        precio_publico = ?,
                        precio_proveedor = ?,
                        existencia = ?
                    WHERE id = ?
                """, (nuevo_precio, nuevo_precio_prov, nueva_existencia, id_sel))
                
                db.commit()
                messagebox.showinfo("Éxito", "Artículo actualizado")
                top.destroy()
                mostrar_articulos()
            except ValueError as e:
                messagebox.showerror("Error", f"Dato inválido: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {e}")

        def eliminar():
            if messagebox.askyesno("Confirmar", "¿Eliminar este artículo permanentemente?"):
                try:
                    cur.execute("DELETE FROM articulos WHERE id=?", (id_sel,))
                    db.commit()
                    messagebox.showinfo("Éxito", "Artículo eliminado")
                    top.destroy()
                    mostrar_articulos()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar: {e}")

        btn_frame = ttk.Frame(top)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
        ttk.Button(btn_frame, text="Guardar", command=actualizar).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Eliminar", command=eliminar).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=top.destroy).pack(side="left", padx=10)

    btn_frame = ttk.Frame(frame_principal)
    btn_frame.pack(pady=10)
    ttk.Button(btn_frame, text="Editar Artículo", command=editar_articulo).pack(side="left", padx=10)
    ttk.Button(btn_frame, text="Volver al Menú", command=mostrar_menu).pack(side="left", padx=10)

'''
Metodo de compra de articulos

'''
def realizar_compra():
    limpiar_ventana()
    root.geometry("600x500")
    
    frame_principal = ttk.Frame(root)
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    ttk.Label(frame_principal, text="Realizar Compra", font=("Arial", 14)).pack(pady=10)

    # Selección de cliente
    frame_cliente = ttk.Frame(frame_principal)
    frame_cliente.pack(fill=tk.X, pady=5)
    ttk.Label(frame_cliente, text="Seleccionar Cliente:").pack(side="left")
    cliente_combo = ttk.Combobox(frame_cliente)
    cliente_combo.pack(side="left", fill=tk.X, expand=True, padx=10)
    
    cur = db.cursor()
    cur.execute("SELECT * FROM clientes")
    clientes = [ClienteFactory.from_row(r) for r in cur.fetchall()]
    cliente_combo["values"] = [f"{c.identificador} - {c.nombre} {c.apellido}" for c in clientes]

    # Lista de artículos
    frame_articulos = ttk.Frame(frame_principal)
    frame_articulos.pack(fill=tk.BOTH, expand=True, pady=10)
    ttk.Label(frame_articulos, text="Seleccionar Artículos:").pack(anchor="w")
    
    articulo_vars = []
    cur.execute("SELECT * FROM articulos WHERE existencia>0")
    articulos = [ArticuloFactory.from_row(r) for r in cur.fetchall()]
    
    for art in articulos:
        fr = ttk.Frame(frame_articulos)
        fr.pack(fill=tk.X, padx=5, pady=2)
        
        v = tk.IntVar()
        ttk.Checkbutton(fr, text=f"{art.nombre} (${art.precio_publico:.2f}) - Stock:{art.existencia}",
                       variable=v).pack(side="left")
        
        sp = ttk.Spinbox(fr, from_=0, to=art.existencia, width=5)
        sp.pack(side="left", padx=10)
        
        articulo_vars.append((art, v, sp))

    def comprar():
        # Validar cliente seleccionado
        idx = cliente_combo.current()
        if idx == -1:
            messagebox.showerror("Error", "Selecciona un cliente")
            return
        
        # Obtener artículos seleccionados
        items_compra = []
        total = 0.0
        
        for art, var, sp in articulo_vars:
            if var.get():
                try:
                    cant = int(sp.get())
                    if cant <= 0:
                        messagebox.showerror("Error", f"Cantidad debe ser mayor que 0 para {art.nombre}")
                        return
                    if cant > art.existencia:
                        messagebox.showerror("Error", f"No hay suficiente stock de {art.nombre}")
                        return
                    
                    items_compra.append((art, cant))
                    total += art.precio_publico * cant
                    
                except ValueError:
                    messagebox.showerror("Error", f"Cantidad inválida para {art.nombre}")
                    return

        if not items_compra:
            messagebox.showerror("Error", "No seleccionaste artículos")
            return

        # Confirmar compra
        if not messagebox.askyesno("Confirmar", f"Total: ${total:.2f}\n¿Desea procesar la compra?"):
            return

        # Actualizar inventario
        cur = db.cursor()
        try:
            for art, cant in items_compra:
                nuevo_stock = art.existencia - cant
                cur.execute("UPDATE articulos SET existencia=? WHERE id=?", (nuevo_stock, art.identificador))
            
            db.commit()
            
            # Generar y mostrar ticket
            ticket = generar_ticket(clientes[idx], items_compra, total)
            messagebox.showinfo("Ticket de Compra", ticket)
            mostrar_menu()
            
        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", f"No se pudo completar la compra: {str(e)}")

    # Botones
    frame_botones = ttk.Frame(frame_principal)
    frame_botones.pack(pady=10)
    ttk.Button(frame_botones, text="Comprar", command=comprar).pack(side="left", padx=10)
    ttk.Button(frame_botones, text="Cancelar", command=mostrar_menu).pack(side="left", padx=10)

# Arranque de la  aplicacion
root = tk.Tk()
root.title("Abarrotes Tizimín")
mostrar_menu()
root.mainloop()