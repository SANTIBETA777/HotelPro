import tkinter as tk
from tkinter import ttk, messagebox
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

class CheckInCheckOutUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        aplicar_estilos(parent)
        self.configure(style="Custom.TFrame")

        ttk.Label(self, text="Gestión de Check-In / Check-Out", style="Titulo.TLabel").pack(pady=10)

        # ------------------ Formulario desplazable ------------------
        scroll_form = ScrollFrame(self)
        scroll_form.pack(pady=10, fill="x", padx=8)

        form_frame = scroll_form.interior

        # Campos
        ttk.Label(form_frame, text="Reserva Nº:", style="Campo.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.reserva_entry = ttk.Entry(form_frame); self.reserva_entry.grid(row=0, column=1, pady=5)
        Tooltip(self.reserva_entry, "Número de la reserva asociada al movimiento")

        ttk.Label(form_frame, text="Habitación Nº:", style="Campo.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.habitacion_entry = ttk.Entry(form_frame); self.habitacion_entry.grid(row=1, column=1, pady=5)
        Tooltip(self.habitacion_entry, "Número de la habitación asignada")

        ttk.Label(form_frame, text="Tipo Movimiento:", style="Campo.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.tipo_entry = ttk.Entry(form_frame); self.tipo_entry.grid(row=2, column=1, pady=5)
        Tooltip(self.tipo_entry, "Indica si es Check-In o Check-Out")

        ttk.Label(form_frame, text="Empleado:", style="Campo.TLabel").grid(row=3, column=0, sticky="w", pady=5)
        self.empleado_entry = ttk.Entry(form_frame); self.empleado_entry.grid(row=3, column=1, pady=5)
        Tooltip(self.empleado_entry, "Nombre del empleado que registra el movimiento")

        ttk.Label(form_frame, text="Observaciones:", style="Campo.TLabel").grid(row=4, column=0, sticky="w", pady=5)
        self.obs_entry = ttk.Entry(form_frame); self.obs_entry.grid(row=4, column=1, pady=5)
        Tooltip(self.obs_entry, "Notas adicionales sobre el movimiento")

        # Botones
        ttk.Button(form_frame, text="✔️ Registrar Movimiento",
                   command=self.agregar_movimiento, style="Registrar.TButton").grid(row=5, column=0, sticky="w", padx=5, pady=15)
        ttk.Button(form_frame, text="✏️ Editar Movimiento",
                   command=self.editar_movimiento, style="Editar.TButton").grid(row=5, column=1, padx=5, pady=10)
        ttk.Button(form_frame, text="🔍 Buscar Movimiento",
                   command=self.buscar_movimiento, style="Buscar.TButton").grid(row=5, column=2, padx=5, pady=10)
        ttk.Button(form_frame, text="❌ Eliminar Movimiento",
                   command=self.eliminar_movimiento, style="Eliminar.TButton").grid(row=5, column=3, padx=5, pady=10)

        # ------------------ Tabla con scroll vertical y horizontal ------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10, padx=8)

        columns = ("id", "reserva", "habitacion", "tipo", "fecha", "empleado")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        # Encabezados (mantener textos originales)
        for col in columns:
            self.tree.heading(col, text=col.capitalize())

        # Anchos iniciales razonables
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("reserva", width=120, anchor="w")
        self.tree.column("habitacion", width=120, anchor="w")
        self.tree.column("tipo", width=120, anchor="center")
        self.tree.column("fecha", width=160, anchor="center")
        self.tree.column("empleado", width=180, anchor="w")

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

        # Hover en filas
        def on_motion(event):
            row_id = self.tree.identify_row(event.y)
            self.tree.tag_configure("hover", background="#ffe680")
            for item in self.tree.get_children():
                self.tree.item(item, tags=())
            if row_id:
                self.tree.item(row_id, tags=("hover",))
        self.tree.bind("<Motion>", on_motion)

        # Soporte scroll horizontal con Shift + rueda del ratón
        def _on_shift_mousewheel(event):
            self.tree.xview_scroll(int(-1 * (event.delta / 120)), "units")
        self.tree.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

        # Cargar movimientos desde la BD
        self.cargar_movimientos()

    # Métodos CRUD
    def agregar_movimiento(self):
        reserva_numero = self.reserva_entry.get()
        habitacion_numero = self.habitacion_entry.get()
        tipo = self.tipo_entry.get()
        empleado = self.empleado_entry.get()
        observaciones = self.obs_entry.get()

        if not reserva_numero or not habitacion_numero or not tipo:
            messagebox.showwarning("Error", "Los campos obligatorios no pueden estar vacíos")
            return

        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO movimientos (reserva_numero, habitacion_numero, tipo, fecha_hora, empleado, observaciones)
                VALUES (%s, %s, %s, NOW(), %s, %s)
            """, (reserva_numero, habitacion_numero, tipo, empleado, observaciones))
            conn.commit()
            row_id = len(self.tree.get_children())
            tag = "evenrow" if row_id % 2 == 0 else "oddrow"
            self.tree.insert("", "end",
                             values=(cursor.lastrowid, reserva_numero, habitacion_numero,
                                     tipo, "Ahora", empleado),
                             tags=(tag,))
            # desplazar y seleccionar la última fila
            children = self.tree.get_children()
            if children:
                last = children[-1]
                self.tree.see(last)
                self.tree.selection_set(last)
            messagebox.showinfo("Éxito", f"{tipo} registrado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar: {e}")
        finally:
            conn.close()

    def cargar_movimientos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, reserva_numero, habitacion_numero, tipo, fecha_hora, empleado FROM movimientos")
            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))
            # Opcional: desplazar al primer elemento para que la vista quede estable
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar movimientos: {e}")
        finally:
            conn.close()

    def editar_movimiento(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Selecciona un movimiento para editar")
            return
        item = self.tree.item(selected[0]); movimiento_id = item["values"][0]
        reserva_numero = self.reserva_entry.get(); habitacion_numero = self.habitacion_entry.get()
        tipo = self.tipo_entry.get(); empleado = self.empleado_entry.get(); observaciones = self.obs_entry.get()
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE movimientos
                SET reserva_numero=%s, habitacion_numero=%s, tipo=%s, empleado=%s, observaciones=%s
                WHERE id=%s
            """, (reserva_numero, habitacion_numero, tipo, empleado, observaciones, movimiento_id))
            conn.commit()
            self.tree.item(selected[0], values=(movimiento_id, reserva_numero, habitacion_numero, tipo, "Ahora", empleado))
            # asegurar que el elemento editado sea visible
            self.tree.see(selected[0])
            messagebox.showinfo("Éxito", "Movimiento actualizado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar: {e}")
        finally:
            conn.close()

    def eliminar_movimiento(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Selecciona un movimiento para eliminar")
            return
        item = self.tree.item(selected[0]); movimiento_id = item["values"][0]
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM movimientos WHERE id=%s", (movimiento_id,))
            conn.commit()
            self.tree.delete(selected[0])
            messagebox.showinfo("Éxito", "Movimiento eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")
        finally:
            conn.close()

    def buscar_movimiento(self):
        criterio = self.reserva_entry.get()
        if not criterio:
            messagebox.showwarning("Error", "Ingresa un número de reserva para buscar")
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, reserva_numero, habitacion_numero, tipo, fecha_hora, empleado
                FROM movimientos WHERE reserva_numero LIKE %s
            """, (f"%{criterio}%",))
            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))
            # mostrar el primer resultado encontrado
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar: {e}")
        finally:
            conn.close()
