# clientes_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from modulos.cliente import Cliente
from database import get_connection
from ui.tooltip import Tooltip
from ui.style import aplicar_estilos

# ------------------ ScrollFrame para formularios largos ------------------
class ScrollFrame(ttk.Frame):
    """Frame con canvas para permitir scroll vertical del formulario."""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.interior = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.interior, anchor="nw")

        def _on_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.interior.bind("<Configure>", _on_configure)

        def _on_mousewheel(event):
            delta = event.delta
            if delta == 0:
                return
            self.canvas.yview_scroll(int(-1 * (delta / 120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

class ClientesUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        aplicar_estilos(parent)

        ttk.Label(self, text="Gestión de Clientes", style="Titulo.TLabel").pack(pady=10)

        # ------------------ Formulario desplazable ------------------
        scroll_form = ScrollFrame(self)
        scroll_form.pack(pady=10, fill="x", padx=8)

        form_frame = scroll_form.interior

        labels = [
            ("ID Cliente:", "id", "Identificador único del cliente"),
            ("Nombres:", "nombres", "Nombres completos del cliente"),
            ("Apellidos:", "apellidos", "Apellidos completos del cliente"),
            ("Documento:", "documento", "Número de identificación oficial"),
            ("Nacionalidad:", "nacionalidad", "País de origen del cliente"),
            ("Fecha Nacimiento:", "fecha_nacimiento", "Formato: AAAA-MM-DD"),
            ("Dirección:", "direccion", "Dirección de residencia"),
            ("Teléfono:", "telefono", "Número de contacto"),
            ("Correo:", "correo", "Correo electrónico válido"),
            ("Nivel Fidelización:", "nivel", "Nivel de puntos o categoría del cliente")
        ]

        self.entries = {}
        for i, (label, key, tip) in enumerate(labels):
            ttk.Label(form_frame, text=label, style="Campo.TLabel").grid(row=i, column=0, sticky="w", pady=3)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, pady=3)
            Tooltip(entry, tip)
            self.entries[key] = entry

        ttk.Button(form_frame, text="✔️ Registrar Cliente",
                   command=self.agregar_cliente, style="Registrar.TButton").grid(
            row=len(labels), column=0, padx=5, pady=10
        )
        ttk.Button(form_frame, text="✏️ Editar Cliente",
                   command=self.editar_cliente, style="Editar.TButton").grid(
            row=len(labels), column=1, padx=5, pady=10
        )
        ttk.Button(form_frame, text="🔍 Buscar Cliente",
                   command=self.buscar_cliente, style="Buscar.TButton").grid(
            row=len(labels), column=2, padx=5, pady=10
        )
        ttk.Button(form_frame, text="❌ Eliminar Cliente",
                   command=self.eliminar_cliente, style="Eliminar.TButton").grid(
            row=len(labels), column=3, padx=5, pady=10
        )

        # ------------------ Tabla con scroll vertical y horizontal ------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10, padx=8)

        columns = [key for _, key, _ in labels]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        for _, key, _ in labels:
            self.tree.heading(key, text=key.capitalize())

        # Anchos iniciales razonables (ajusta según necesites)
        # Mantener el mismo orden que columns
        widths = {
            "id": 100, "nombres": 180, "apellidos": 180, "documento": 120,
            "nacionalidad": 120, "fecha_nacimiento": 120, "direccion": 220,
            "telefono": 120, "correo": 200, "nivel": 120
        }
        for col in columns:
            w = widths.get(col, 120)
            anchor = "w" if col not in ("id", "nivel", "fecha_nacimiento") else "center"
            self.tree.column(col, width=w, anchor=anchor)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.tag_configure("oddrow", background="#ffffff")
        self.tree.tag_configure("evenrow", background="#d9edf7")

        def on_motion(event):
            row_id = self.tree.identify_row(event.y)
            self.tree.tag_configure("hover", background="#ffe680")
            for item in self.tree.get_children():
                self.tree.item(item, tags=())
            if row_id:
                self.tree.item(row_id, tags=("hover",))
        self.tree.bind("<Motion>", on_motion)

        def _on_shift_mousewheel(event):
            self.tree.xview_scroll(int(-1 * (event.delta / 120)), "units")
        self.tree.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

        self.cargar_clientes()

    # Métodos CRUD
    def agregar_cliente(self):
        datos = {key: entry.get() for key, entry in self.entries.items()}
        if not datos["id"] or not datos["nombres"] or not datos["apellidos"] or not datos["correo"]:
            messagebox.showwarning("Error", "ID, nombres, apellidos y correo son obligatorios")
            return

        cliente = Cliente(
            datos["id"], datos["nombres"], datos["apellidos"], datos["documento"], datos["nacionalidad"],
            datos["fecha_nacimiento"], datos["direccion"], datos["telefono"], datos["correo"],
            [], int(datos["nivel"]) if datos["nivel"] else 0
        )

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO clientes (id, nombres, apellidos, documento, nacionalidad, fecha_nacimiento, direccion, telefono, correo, nivel_fidelizacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (cliente.id_cliente, cliente.nombres, cliente.apellidos, cliente.documento, cliente.nacionalidad,
                  cliente.fecha_nacimiento, cliente.direccion, cliente.telefono, cliente.correo, cliente.nivel_fidelizacion))
            conn.commit()
            row_id = len(self.tree.get_children())
            tag = "evenrow" if row_id % 2 == 0 else "oddrow"
            # Insertar en treeview y desplazar a la última fila
            self.tree.insert("", "end", values=tuple(datos.values()), tags=(tag,))
            children = self.tree.get_children()
            if children:
                last = children[-1]
                self.tree.see(last)
                self.tree.selection_set(last)
            messagebox.showinfo("Éxito", f"Cliente {cliente.nombres} registrado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")
        finally:
            conn.close()

    def cargar_clientes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nombres, apellidos, documento, nacionalidad, fecha_nacimiento, direccion, telefono, correo, nivel_fidelizacion FROM clientes")
            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar clientes: {e}")
        finally:
            conn.close()

    def editar_cliente(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un cliente para editar")
            return
        cliente_id = self.tree.item(selected[0], "values")[0]
        datos = {key: entry.get() for key, entry in self.entries.items()}
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE clientes
                SET nombres=%s, apellidos=%s, documento=%s, nacionalidad=%s, fecha_nacimiento=%s,
                    direccion=%s, telefono=%s, correo=%s, nivel_fidelizacion=%s
                WHERE id=%s
            """, (datos["nombres"], datos["apellidos"], datos["documento"], datos["nacionalidad"],
                  datos["fecha_nacimiento"], datos["direccion"], datos["telefono"], datos["correo"],
                  int(datos["nivel"]) if datos["nivel"] else 0, cliente_id))
            conn.commit()
            self.cargar_clientes()
            messagebox.showinfo("Éxito", f"Cliente {cliente_id} actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el cliente: {e}")
        finally:
            conn.close()

    def eliminar_cliente(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un cliente para eliminar")
            return
        cliente_id = self.tree.item(selected[0], "values")[0]
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM clientes WHERE id=%s", (cliente_id,))
            conn.commit()
            self.cargar_clientes()
            messagebox.showinfo("Éxito", f"Cliente {cliente_id} eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")
        finally:
            conn.close()

    def buscar_cliente(self):
        criterio = self.entries["id"].get()
        if not criterio:
            messagebox.showwarning("Error", "Ingrese un ID de cliente para buscar")
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, nombres, apellidos, documento, nacionalidad, fecha_nacimiento, direccion, telefono, correo, nivel_fidelizacion
                FROM clientes WHERE id=%s
            """, (criterio,))
            row = cursor.fetchone()
            if row:
                self.tree.insert("", "end", values=row)
                children = self.tree.get_children()
                if children:
                    self.tree.see(children[0])
            else:
                messagebox.showinfo("Resultado", f"No se encontró cliente con ID {criterio}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el cliente: {e}")
        finally:
            conn.close()
