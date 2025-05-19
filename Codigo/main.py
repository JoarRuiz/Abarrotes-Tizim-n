import tkinter as tk
from tkinter import ttk, messagebox
from controller import SistemaAbarrotesController

class SistemaAbarrotesUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Abarrotes Tizimín")
        self.controller = SistemaAbarrotesController()
        self.mostrar_menu()

    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_menu(self):
        self.limpiar_ventana()
        self.root.geometry("400x300")
        
        ttk.Label(self.root, text="Menú Principal", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self.root, text="Registrar Cliente", command=self.registrar_cliente, width=20).pack(pady=10)
        ttk.Button(self.root, text="Registrar Artículo", command=self.registrar_articulo, width=20).pack(pady=10)
        ttk.Button(self.root, text="Realizar Compra", command=self.realizar_compra, width=20).pack(pady=10)
        ttk.Button(self.root, text="Salir", command=self.root.destroy, width=20).pack(pady=10)

    def registrar_cliente(self):
        self.limpiar_ventana()
        self.root.geometry("500x550")
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(frame_principal, text="Registro de Cliente", font=("Arial", 14)).pack(pady=10)

        campos = ["ID", "Nombre", "Apellido", "Calle", "Número", 
                "Colonia", "CP", "Ciudad", "Estado", "Teléfono"]
        self.entradas_cliente = {}
        
        for campo in campos:
            ttk.Label(frame_principal, text=campo).pack()
            entrada = ttk.Entry(frame_principal)
            entrada.pack()
            self.entradas_cliente[campo] = entrada

        def guardar():
            datos = [self.entradas_cliente[campo].get() for campo in campos]
            try:
                mensaje = self.controller.registrar_cliente(tuple(datos))
                messagebox.showinfo("Éxito", mensaje)
                self.mostrar_clientes()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=15)
        ttk.Button(frame_botones, text="Guardar Cliente", command=guardar).grid(row=0, column=0, padx=10)
        ttk.Button(frame_botones, text="Cancelar", command=self.mostrar_menu).grid(row=0, column=1, padx=10)
        ttk.Button(frame_botones, text="Ver Clientes", command=self.mostrar_clientes).grid(row=0, column=2, padx=10)

    def mostrar_clientes(self):
        self.limpiar_ventana()
        self.root.geometry("1000x500")
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame_principal, text="Clientes Registrados", font=("Arial", 14)).pack(pady=10)

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

        self.tree_clientes = ttk.Treeview(frame_tabla, columns=[col[0] for col in columnas], show="headings", height=15)

        for col, width in columnas:
            self.tree_clientes.heading(col, text=col)
            self.tree_clientes.column(col, width=width, anchor="w")

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_clientes.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)
        self.tree_clientes.pack(side="left", fill=tk.BOTH, expand=True)

        try:
            clientes = self.controller.obtener_clientes()
            for cliente in clientes:
                self.tree_clientes.insert("", tk.END, values=(
                    cliente.identificador,
                    cliente.nombre,
                    cliente.apellido,
                    cliente.telefono,
                    cliente.calle,
                    cliente.numero,
                    cliente.colonia,
                    cliente.cp,
                    cliente.ciudad,
                    cliente.estado
                ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar clientes: {str(e)}")
            self.mostrar_menu()
            return

        def editar_cliente():
            item = self.tree_clientes.focus()
            if not item:
                messagebox.showerror("Error", "Selecciona un cliente")
                return
            
            cliente_data = self.tree_clientes.item(item)["values"]
            self.editar_cliente_ventana(cliente_data[0])

        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=10)
        ttk.Button(frame_botones, text="Editar Cliente", command=editar_cliente).pack(side="left", padx=10)
        ttk.Button(frame_botones, text="Volver al Menú", command=self.mostrar_menu).pack(side="left", padx=10)

    def editar_cliente_ventana(self, cliente_id):
        try:
            cliente = self.controller._obtener_cliente_por_id(cliente_id)
            
            top = tk.Toplevel(self.root)
            top.title("Editar Cliente")
            top.geometry("400x500")
            
            # Información no editable
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
                    datos_actualizados = (
                        entries["Calle"].get(),
                        entries["Número"].get(),
                        entries["Colonia"].get(),
                        entries["CP"].get(),
                        entries["Ciudad"].get(),
                        entries["Estado"].get(),
                        entries["Teléfono"].get(),
                        cliente_id
                    )
                    
                    cur = self.controller.db.cursor()
                    cur.execute("""
                        UPDATE clientes SET
                            calle=?, numero=?, colonia=?,
                            cp=?, ciudad=?, estado=?, telefono=?
                        WHERE id=?
                    """, datos_actualizados)
                    self.controller.db.commit()
                    
                    messagebox.showinfo("Éxito", "Cliente actualizado")
                    top.destroy()
                    self.mostrar_clientes()
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar: {str(e)}")

            btn_frame = ttk.Frame(top)
            btn_frame.grid(row=len(campos_editables)+4, column=0, columnspan=2, pady=15)
            ttk.Button(btn_frame, text="Guardar", command=actualizar).pack(side="left", padx=10)
            ttk.Button(btn_frame, text="Cancelar", command=top.destroy).pack(side="left", padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar cliente: {str(e)}")

    def registrar_articulo(self):
        self.limpiar_ventana()
        self.root.geometry("500x400")
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(frame_principal, text="Registro de Artículo", font=("Arial", 14)).pack(pady=10)

        campos = ["ID", "Nombre", "Precio Público", "Precio Proveedor", "Existencia"]
        self.entradas_articulo = {}
        
        for campo in campos:
            ttk.Label(frame_principal, text=campo).pack()
            entrada = ttk.Entry(frame_principal)
            entrada.pack()
            self.entradas_articulo[campo] = entrada

        def guardar():
            datos = (
                self.entradas_articulo["ID"].get(),
                self.entradas_articulo["Nombre"].get(),
                self.entradas_articulo["Precio Público"].get(),
                self.entradas_articulo["Precio Proveedor"].get(),
                self.entradas_articulo["Existencia"].get()
            )
            
            try:
                mensaje = self.controller.registrar_articulo(datos)
                messagebox.showinfo("Éxito", mensaje)
                self.mostrar_articulos()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=15)
        ttk.Button(frame_botones, text="Guardar Artículo", command=guardar).grid(row=0, column=0, padx=10)
        ttk.Button(frame_botones, text="Cancelar", command=self.mostrar_menu).grid(row=0, column=1, padx=10)
        ttk.Button(frame_botones, text="Ver Artículos", command=self.mostrar_articulos).grid(row=0, column=2, padx=10)

    def mostrar_articulos(self):
        self.limpiar_ventana()
        self.root.geometry("700x500")
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(frame_principal, text="Artículos Registrados", font=("Arial", 14)).pack(pady=10)

        frame_tabla = ttk.Frame(frame_principal)
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columnas = [
            ("ID", 100),
            ("Nombre", 250),
            ("Precio Público", 150),
            ("Precio Proveedor", 150),
            ("Existencia", 100)
        ]

        self.tree_articulos = ttk.Treeview(frame_tabla, columns=[col[0] for col in columnas], show="headings", height=15)

        for col, width in columnas:
            self.tree_articulos.heading(col, text=col)
            anchor = "e" if col in ["Precio Público", "Precio Proveedor", "Existencia"] else "w"
            self.tree_articulos.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_articulos.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_articulos.configure(yscrollcommand=scrollbar.set)
        self.tree_articulos.pack(side="left", fill=tk.BOTH, expand=True)

        try:
            articulos = self.controller.obtener_articulos()
            for art in articulos:
                self.tree_articulos.insert("", tk.END, values=(
                    art.identificador,
                    art.nombre,
                    f"${art.precio_publico:.2f}",
                    f"${art.precio_proveedor:.2f}",
                    art.existencia
                ))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar artículos: {str(e)}")
            self.mostrar_menu()
            return

        def editar_articulo():
            item = self.tree_articulos.focus()
            if not item:
                messagebox.showerror("Error", "Selecciona un artículo")
                return
            
            art_id = self.tree_articulos.item(item)["values"][0]
            self.editar_articulo_ventana(art_id)

        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=10)
        ttk.Button(frame_botones, text="Editar Artículo", command=editar_articulo).pack(side="left", padx=10)
        ttk.Button(frame_botones, text="Volver al Menú", command=self.mostrar_menu).pack(side="left", padx=10)

    def editar_articulo_ventana(self, art_id):
        try:
            articulo = self.controller._obtener_articulo_por_id(art_id)
            
            top = tk.Toplevel(self.root)
            top.title("Editar Artículo")
            top.geometry("300x300")
            
            # Información no editable
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
                        
                    cur = self.controller.db.cursor()
                    cur.execute("""
                        UPDATE articulos SET
                            precio_publico = ?,
                            precio_proveedor = ?,
                            existencia = ?
                        WHERE id = ?
                    """, (nuevo_precio, nuevo_precio_prov, nueva_existencia, art_id))
                    
                    self.controller.db.commit()
                    messagebox.showinfo("Éxito", "Artículo actualizado")
                    top.destroy()
                    self.mostrar_articulos()
                except ValueError as e:
                    messagebox.showerror("Error", f"Dato inválido: {e}")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar: {e}")

            btn_frame = ttk.Frame(top)
            btn_frame.grid(row=5, column=0, columnspan=2, pady=15)
            ttk.Button(btn_frame, text="Guardar", command=actualizar).pack(side="left", padx=10)
            ttk.Button(btn_frame, text="Cancelar", command=top.destroy).pack(side="left", padx=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar artículo: {str(e)}")

    def realizar_compra(self):
        self.limpiar_ventana()
        self.root.geometry("600x500")
        
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(frame_principal, text="Realizar Compra", font=("Arial", 14)).pack(pady=10)

        # Selección de cliente
        frame_cliente = ttk.Frame(frame_principal)
        frame_cliente.pack(fill=tk.X, pady=5)
        ttk.Label(frame_cliente, text="Cliente:").pack(side="left")
        
        self.cliente_combo = ttk.Combobox(frame_cliente, state="readonly")
        self.cliente_combo.pack(side="left", fill=tk.X, expand=True, padx=10)
        
        try:
            clientes = self.controller.obtener_clientes()
            self.cliente_combo["values"] = [f"{c.identificador} - {c.nombre} {c.apellido}" for c in clientes]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar clientes: {str(e)}")
            self.mostrar_menu()
            return

        # Lista de artículos disponibles
        frame_articulos = ttk.Frame(frame_principal)
        frame_articulos.pack(fill=tk.BOTH, expand=True, pady=10)
        ttk.Label(frame_articulos, text="Artículos Disponibles:").pack(anchor="w")

        self.articulos_vars = []
        try:
            articulos = self.controller.obtener_articulos_disponibles()
            
            for art in articulos:
                frame_art = ttk.Frame(frame_articulos)
                frame_art.pack(fill=tk.X, padx=5, pady=2)
                
                var = tk.IntVar()
                check = ttk.Checkbutton(
                    frame_art, 
                    text=f"{art.nombre} (${art.precio_publico:.2f}) - Stock: {art.existencia}", 
                    variable=var
                )
                check.pack(side="left")
                
                spin = ttk.Spinbox(frame_art, from_=0, to=art.existencia, width=5)
                spin.pack(side="left", padx=10)
                
                self.articulos_vars.append((art, var, spin))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar artículos: {str(e)}")
            self.mostrar_menu()
            return

        def procesar_compra():
            try:
                cliente_idx = self.cliente_combo.current()
                if cliente_idx == -1:
                    raise ValueError("Selecciona un cliente")
                
                items_compra = []
                for art, var, spin in self.articulos_vars:
                    if var.get():
                        cantidad = int(spin.get())
                        if cantidad <= 0:
                            raise ValueError(f"Cantidad no válida para {art.nombre}")
                        items_compra.append((art.identificador, cantidad))

                if not items_compra:
                    raise ValueError("Selecciona al menos un artículo")

                cliente_id = clientes[cliente_idx].identificador
                ticket = self.controller.procesar_compra(cliente_id, items_compra)
                messagebox.showinfo("Ticket de Compra", ticket)
                self.mostrar_menu()
                
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")

        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=10)
        ttk.Button(frame_botones, text="Comprar", command=procesar_compra).pack(side="left", padx=10)
        ttk.Button(frame_botones, text="Cancelar", command=self.mostrar_menu).pack(side="left", padx=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaAbarrotesUI(root)
    root.mainloop()