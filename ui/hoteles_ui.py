# hoteles_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from modulos.hotel import Hotel
from database import get_connection
from ui.tooltip import Tooltip   # clase Tooltip que ya usabas
from ui.style import aplicar_estilos   # función de estilos que ya usabas

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
            # actualizar la región de scroll
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.interior.bind("<Configure>", _on_configure)

        # Soporte rueda del ratón (Windows / Mac)
        def _on_mousewheel(event):
            delta = event.delta
            if delta == 0:
                return
            self.canvas.yview_scroll(int(-1 * (delta / 120)), "units")
        # bind_all para que funcione aunque el foco no esté exactamente en el canvas
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

# ------------------ Interfaz principal ------------------
class HotelesUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Aplicar estilos al root (como ya tenías)
        aplicar_estilos(parent)

        # Encabezado con estilo
        ttk.Label(self, text="Gestión de Hoteles", style="Titulo.TLabel").pack(pady=10)

        # ------------------ Formulario desplazable ------------------
        scroll_form = ScrollFrame(self)
        scroll_form.pack(pady=10, fill="x", padx=8)

        form_frame = scroll_form.interior

        # Campos del formulario con estilo + tooltips (igual que antes, solo cambia el contenedor)
        ttk.Label(form_frame, text="Código:", style="Campo.TLabel").grid(row=0, column=0, sticky="w", pady=3)
        self.codigo_entry = ttk.Entry(form_frame)
        self.codigo_entry.grid(row=0, column=1, pady=3)
        Tooltip(self.codigo_entry, "Identificador único del hotel")

        ttk.Label(form_frame, text="Nombre:", style="Campo.TLabel").grid(row=1, column=0, sticky="w", pady=3)
        self.nombre_entry = ttk.Entry(form_frame)
        self.nombre_entry.grid(row=1, column=1, pady=3)
        Tooltip(self.nombre_entry, "Nombre oficial del hotel")

        ttk.Label(form_frame, text="Categoría (★):", style="Campo.TLabel").grid(row=2, column=0, sticky="w", pady=3)
        self.categoria_entry = ttk.Entry(form_frame)
        self.categoria_entry.grid(row=2, column=1, pady=3)
        Tooltip(self.categoria_entry, "Clasificación del hotel en estrellas (ej. 5)")

        ttk.Label(form_frame, text="Dirección:", style="Campo.TLabel").grid(row=3, column=0, sticky="w", pady=3)
        self.direccion_entry = ttk.Entry(form_frame)
        self.direccion_entry.grid(row=3, column=1, pady=3)
        Tooltip(self.direccion_entry, "Dirección completa del hotel")

        ttk.Label(form_frame, text="Teléfono:", style="Campo.TLabel").grid(row=4, column=0, sticky="w", pady=3)
        self.telefono_entry = ttk.Entry(form_frame)
        self.telefono_entry.grid(row=4, column=1, pady=3)
        Tooltip(self.telefono_entry, "Número de contacto del hotel")

        ttk.Label(form_frame, text="Correo:", style="Campo.TLabel").grid(row=5, column=0, sticky="w", pady=3)
        self.correo_entry = ttk.Entry(form_frame)
        self.correo_entry.grid(row=5, column=1, pady=3)
        Tooltip(self.correo_entry, "Correo electrónico de contacto")

        ttk.Label(form_frame, text="Año Inauguración:", style="Campo.TLabel").grid(row=6, column=0, sticky="w", pady=3)
        self.anio_entry = ttk.Entry(form_frame)
        self.anio_entry.grid(row=6, column=1, pady=3)
        Tooltip(self.anio_entry, "Año en que se inauguró el hotel (ej. 2010)")

        ttk.Label(form_frame, text="Habitaciones:", style="Campo.TLabel").grid(row=7, column=0, sticky="w", pady=3)
        self.num_habitaciones_entry = ttk.Entry(form_frame)
        self.num_habitaciones_entry.grid(row=7, column=1, pady=3)
        Tooltip(self.num_habitaciones_entry, "Número total de habitaciones")

        ttk.Label(form_frame, text="Servicios:", style="Campo.TLabel").grid(row=8, column=0, sticky="w", pady=3)
        self.servicios_entry = ttk.Entry(form_frame)
        self.servicios_entry.grid(row=8, column=1, pady=3)
        Tooltip(self.servicios_entry, "Servicios separados por comas (ej. wifi,piscina,spa)")

        ttk.Label(form_frame, text="Horarios:", style="Campo.TLabel").grid(row=9, column=0, sticky="w", pady=3)
        self.horarios_entry = ttk.Entry(form_frame)
        self.horarios_entry.grid(row=9, column=1, pady=3)
        Tooltip(self.horarios_entry, "Horario de atención (ej. 24/7, 08:00-22:00)")

        ttk.Label(form_frame, text="Gerente:", style="Campo.TLabel").grid(row=10, column=0, sticky="w", pady=3)
        self.gerente_entry = ttk.Entry(form_frame)
        self.gerente_entry.grid(row=10, column=1, pady=3)
        Tooltip(self.gerente_entry, "Nombre del gerente responsable")

        # Botones con estilos pastel (misma posición lógica que tenías)
        ttk.Button(form_frame, text="✔️ Registrar Hotel",
                    command=self.agregar_hotel, style="Registrar.TButton").grid(row=11, column=0, padx=5, pady=10)

        ttk.Button(form_frame, text="✏️ Editar Hotel",
                    command=self.editar_hotel, style="Editar.TButton").grid(row=11, column=1, padx=5, pady=10)

        ttk.Button(form_frame, text="🔍 Buscar Hotel",
                    command=self.buscar_hotel, style="Buscar.TButton").grid(row=11, column=2, padx=5, pady=10)

        ttk.Button(form_frame, text="❌ Eliminar Hotel",
                    command=self.eliminar_hotel, style="Eliminar.TButton").grid(row=11, column=3, padx=5, pady=10)

        # ------------------ Tabla de hoteles con scroll vertical y horizontal ------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10, padx=8)

        columns = (
            "codigo", "nombre", "categoria", "direccion", "telefono", "correo",
            "anio_inauguracion", "num_habitaciones", "servicios", "horarios", "gerente"
        )

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        # Encabezados
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("direccion", text="Dirección")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("correo", text="Correo")
        self.tree.heading("anio_inauguracion", text="Año Inaug.")
        self.tree.heading("num_habitaciones", text="Habitaciones")
        self.tree.heading("servicios", text="Servicios")
        self.tree.heading("horarios", text="Horarios")
        self.tree.heading("gerente", text="Gerente")

        # Columnas: anchos iniciales razonables
        self.tree.column("codigo", width=80, anchor="w")
        self.tree.column("nombre", width=200, anchor="w")
        self.tree.column("categoria", width=80, anchor="center")
        self.tree.column("direccion", width=250, anchor="w")
        self.tree.column("telefono", width=120, anchor="w")
        self.tree.column("correo", width=200, anchor="w")
        self.tree.column("anio_inauguracion", width=90, anchor="center")
        self.tree.column("num_habitaciones", width=100, anchor="center")
        self.tree.column("servicios", width=220, anchor="w")
        self.tree.column("horarios", width=140, anchor="w")
        self.tree.column("gerente", width=150, anchor="w")

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Layout con grid para que scrollbars y treeview se ajusten
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Colores alternados en filas
        self.tree.tag_configure("oddrow", background="#ffffff")
        self.tree.tag_configure("evenrow", background="#d9edf7")

        # Hover en filas (manteniendo tu lógica)
        def on_motion(event):
            row_id = self.tree.identify_row(event.y)
            self.tree.tag_configure("hover", background="#ffe680")
            for item in self.tree.get_children():
                # mantener solo odd/even si no hover
                tags = ()
                self.tree.item(item, tags=tags)
            if row_id:
                self.tree.item(row_id, tags=("hover",))
        self.tree.bind("<Motion>", on_motion)

        # Soporte scroll horizontal con Shift + rueda del ratón
        def _on_shift_mousewheel(event):
            # event.state & 0x0001 detecta Shift en Windows; si no funciona en tu SO, puedes ajustar
            self.tree.xview_scroll(int(-1 * (event.delta / 120)), "units")
        self.tree.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

        # Cargar hoteles desde la BD
        self.cargar_hoteles()

    # ------------------ Métodos CRUD (sin cambios lógicos, solo ajustes para scroll) ------------------
    def agregar_hotel(self):
        codigo = self.codigo_entry.get()
        nombre = self.nombre_entry.get()
        categoria = self.categoria_entry.get()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()
        correo = self.correo_entry.get()
        anio = self.anio_entry.get()
        habitaciones = self.num_habitaciones_entry.get()
        servicios = self.servicios_entry.get()
        horarios = self.horarios_entry.get()
        gerente = self.gerente_entry.get()

        if not codigo or not nombre or not categoria:
            messagebox.showwarning("Error", "Código, nombre y categoría son obligatorios")
            return

        hotel = Hotel(
            codigo, nombre, categoria, direccion, telefono, correo,
            int(anio) if anio else 0,
            int(habitaciones) if habitaciones else 0,
            servicios, horarios, gerente
        )

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO hoteles (
                    codigo, nombre, categoria, direccion, telefono, correo,
                    anio_inauguracion, num_habitaciones, servicios, horarios, gerente
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                hotel.codigo, hotel.nombre, int(hotel.categoria), hotel.direccion, hotel.telefono, hotel.correo,
                hotel.anio_inauguracion, hotel.num_habitaciones, hotel.servicios, hotel.horarios, hotel.gerente
            ))
            conn.commit()
            # Insertar en el treeview y desplazar para ver la fila nueva
            row_id = len(self.tree.get_children())
            tag = "evenrow" if row_id % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(
                hotel.codigo, hotel.nombre, hotel.categoria, hotel.direccion, hotel.telefono, hotel.correo,
                hotel.anio_inauguracion, hotel.num_habitaciones, hotel.servicios, hotel.horarios, hotel.gerente
            ), tags=(tag,))
            # desplazar y seleccionar la última fila
            children = self.tree.get_children()
            if children:
                last = children[-1]
                self.tree.see(last)
                self.tree.selection_set(last)
            messagebox.showinfo("Éxito", f"Hotel {nombre} registrado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el hotel: {e}")
        finally:
            conn.close()

    def cargar_hoteles(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT codigo, nombre, categoria, direccion, telefono, correo,
                       anio_inauguracion, num_habitaciones, servicios, horarios, gerente
                FROM hoteles
            """)
            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))
            # Opcional: desplazar al primer elemento para que la vista quede estable
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la lista de hoteles: {e}")
        finally:
            conn.close()

    def editar_hotel(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un hotel para editar")
            return

        codigo = self.tree.item(selected[0], "values")[0]

        nombre = self.nombre_entry.get()
        categoria = self.categoria_entry.get()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()
        correo = self.correo_entry.get()
        anio = self.anio_entry.get()
        habitaciones = self.num_habitaciones_entry.get()
        servicios = self.servicios_entry.get()
        horarios = self.horarios_entry.get()
        gerente = self.gerente_entry.get()

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE hoteles SET
                    nombre=%s, categoria=%s, direccion=%s, telefono=%s, correo=%s,
                    anio_inauguracion=%s, num_habitaciones=%s, servicios=%s, horarios=%s, gerente=%s
                WHERE codigo=%s
            """, (
                nombre, int(categoria) if categoria else None, direccion, telefono, correo,
                int(anio) if anio else 0,
                int(habitaciones) if habitaciones else 0,
                servicios, horarios, gerente, codigo
            ))
            conn.commit()
            self.cargar_hoteles()
            messagebox.showinfo("Éxito", f"Hotel {codigo} actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el hotel: {e}")
        finally:
            conn.close()

    def eliminar_hotel(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un hotel para eliminar")
            return

        codigo = self.tree.item(selected[0], "values")[0]

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM hoteles WHERE codigo=%s", (codigo,))
            conn.commit()
            self.cargar_hoteles()
            messagebox.showinfo("Éxito", f"Hotel {codigo} eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el hotel: {e}")
        finally:
            conn.close()

    def buscar_hotel(self):
        codigo = self.codigo_entry.get()
        if not codigo:
            messagebox.showwarning("Error", "Ingrese un código para buscar")
            return

        # Limpiar la tabla antes de mostrar resultados
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT codigo, nombre, categoria, direccion, telefono, correo,
                        anio_inauguracion, num_habitaciones, servicios, horarios, gerente
                FROM hoteles WHERE codigo=%s
            """, (codigo,))
            rows = cursor.fetchall()
            if not rows:
                messagebox.showinfo("Resultado", f"No se encontró hotel con código {codigo}")
                return
            for i, row in enumerate(rows):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))
            # mostrar el primer resultado encontrado
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar el hotel: {e}")
        finally:
            conn.close()
