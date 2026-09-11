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
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.interior.bind("<Configure>", _on_configure)

        def _on_mousewheel(event):
            delta = event.delta
            if delta == 0:
                return
            self.canvas.yview_scroll(int(-1 * (delta / 120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)


class HabitacionesUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        aplicar_estilos(parent)

        ttk.Label(self, text="Gestión de Habitaciones", style="Titulo.TLabel").pack(pady=10)

        # ------------------ Formulario desplazable ------------------
        scroll_form = ScrollFrame(self)
        scroll_form.pack(pady=10, fill="x", padx=8)

        form_frame = scroll_form.interior

        # Campos
        ttk.Label(form_frame, text="Número:", style="Campo.TLabel").grid(row=0, column=0, sticky="w", pady=3)
        self.numero_entry = ttk.Entry(form_frame); self.numero_entry.grid(row=0, column=1, pady=3)
        Tooltip(self.numero_entry, "Número de la habitación dentro del hotel")

        ttk.Label(form_frame, text="Piso:", style="Campo.TLabel").grid(row=1, column=0, sticky="w", pady=3)
        self.piso_entry = ttk.Entry(form_frame); self.piso_entry.grid(row=1, column=1, pady=3)
        Tooltip(self.piso_entry, "Piso en el que se encuentra la habitación")

        ttk.Label(form_frame, text="Tipo:", style="Campo.TLabel").grid(row=2, column=0, sticky="w", pady=3)
        self.tipo_entry = ttk.Entry(form_frame); self.tipo_entry.grid(row=2, column=1, pady=3)
        Tooltip(self.tipo_entry, "Ejemplo: estándar, suite, familiar")

        ttk.Label(form_frame, text="Orientación:", style="Campo.TLabel").grid(row=3, column=0, sticky="w", pady=3)
        self.orientacion_entry = ttk.Entry(form_frame); self.orientacion_entry.grid(row=3, column=1, pady=3)
        Tooltip(self.orientacion_entry, "Vista de la habitación (ej. al mar, a la ciudad)")

        ttk.Label(form_frame, text="Estado:", style="Campo.TLabel").grid(row=4, column=0, sticky="w", pady=3)
        self.estado_entry = ttk.Entry(form_frame); self.estado_entry.grid(row=4, column=1, pady=3)
        Tooltip(self.estado_entry, "Disponible, ocupada o en mantenimiento")

        ttk.Label(form_frame, text="Tarifa Base:", style="Campo.TLabel").grid(row=5, column=0, sticky="w", pady=3)
        self.tarifa_entry = ttk.Entry(form_frame); self.tarifa_entry.grid(row=5, column=1, pady=3)
        Tooltip(self.tarifa_entry, "Precio base por noche")

        ttk.Label(form_frame, text="Hotel Código:", style="Campo.TLabel").grid(row=6, column=0, sticky="w", pady=3)
        self.hotel_entry = ttk.Entry(form_frame); self.hotel_entry.grid(row=6, column=1, pady=3)
        Tooltip(self.hotel_entry, "Código del hotel al que pertenece la habitación")

        # Botones
        ttk.Button(form_frame, text="✔️ Registrar Habitación",
                   command=self.agregar_habitacion, style="Registrar.TButton").grid(row=7, column=0, padx=5, pady=10)
        ttk.Button(form_frame, text="✏️ Editar Habitación",
                   command=self.editar_habitacion, style="Editar.TButton").grid(row=7, column=1, padx=5, pady=10)
        ttk.Button(form_frame, text="🔍 Buscar Habitación",
                   command=self.buscar_habitacion, style="Buscar.TButton").grid(row=7, column=2, padx=5, pady=10)
        ttk.Button(form_frame, text="❌ Eliminar Habitación",
                   command=self.eliminar_habitacion, style="Eliminar.TButton").grid(row=7, column=3, padx=5, pady=10)

        # ------------------ Tabla con scroll vertical y horizontal ------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10, padx=8)

        columns = ("numero", "piso", "tipo", "orientacion", "estado", "tarifa", "hotel")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        for col in columns:
            self.tree.heading(col, text=col.capitalize())

        # Anchos iniciales razonables
        self.tree.column("numero", width=100, anchor="center")
        self.tree.column("piso", width=80, anchor="center")
        self.tree.column("tipo", width=140, anchor="w")
        self.tree.column("orientacion", width=160, anchor="w")
        self.tree.column("estado", width=120, anchor="center")
        self.tree.column("tarifa", width=100, anchor="e")
        self.tree.column("hotel", width=120, anchor="w")

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

        # Soporte scroll horizontal con Shift + rueda del ratón
        def _on_shift_mousewheel(event):
            self.tree.xview_scroll(int(-1 * (event.delta / 120)), "units")
        self.tree.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

        self.cargar_habitaciones()

    # Métodos CRUD
    def agregar_habitacion(self):
        numero = self.numero_entry.get()
        piso = self.piso_entry.get()
        tipo = self.tipo_entry.get()
        orientacion = self.orientacion_entry.get()
        estado = self.estado_entry.get()
        tarifa = self.tarifa_entry.get()
        hotel_codigo = self.hotel_entry.get()

        if not numero or not tipo or not estado or not hotel_codigo:
            messagebox.showwarning("Error", "Los campos obligatorios no pueden estar vacíos")
            return

        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO habitaciones (numero, piso, tipo, orientacion, estado, tarifa_base, hotel_codigo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (numero, piso, tipo, orientacion, estado,
                  float(tarifa) if tarifa else 0, hotel_codigo))
            conn.commit()
            row_id = len(self.tree.get_children())
            tag = "evenrow" if row_id % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(numero, piso, tipo, orientacion, estado, tarifa, hotel_codigo), tags=(tag,))
            # desplazar y seleccionar la última fila
            children = self.tree.get_children()
            if children:
                last = children[-1]
                self.tree.see(last)
                self.tree.selection_set(last)
            messagebox.showinfo("Éxito", f"Habitación {numero} registrada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la habitación: {e}")
        finally:
            conn.close()

    def cargar_habitaciones(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("SELECT numero, piso, tipo, orientacion, estado, tarifa_base, hotel_codigo FROM habitaciones")
            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))
            # Opcional: desplazar al primer elemento para estabilidad
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar habitaciones: {e}")
        finally:
            conn.close()

    def editar_habitacion(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione una habitación para editar")
            return
        numero = self.tree.item(selected[0], "values")[0]
        piso = self.piso_entry.get(); tipo = self.tipo_entry.get()
        orientacion = self.orientacion_entry.get(); estado = self.estado_entry.get()
        tarifa = self.tarifa_entry.get(); hotel_codigo = self.hotel_entry.get()
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE habitaciones
                SET piso=%s, tipo=%s, orientacion=%s, estado=%s, tarifa_base=%s, hotel_codigo=%s
                WHERE numero=%s
            """, (piso, tipo, orientacion, estado,
                  float(tarifa) if tarifa else 0, hotel_codigo, numero))
            conn.commit()
            self.cargar_habitaciones()
            # asegurar que el elemento editado sea visible
            children = self.tree.get_children()
            for ch in children:
                vals = self.tree.item(ch, "values")
                if vals and str(vals[0]) == str(numero):
                    self.tree.see(ch)
                    self.tree.selection_set(ch)
                    break
            messagebox.showinfo("Éxito", f"Habitación {numero} actualizada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la habitación: {e}")
        finally:
            conn.close()

    def eliminar_habitacion(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione una habitación para eliminar")
            return
        numero = self.tree.item(selected[0], "values")[0]
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM habitaciones WHERE numero=%s", (numero,))
            conn.commit()
            self.cargar_habitaciones()
            messagebox.showinfo("Éxito", f"Habitación {numero} eliminada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la habitación: {e}")
        finally:
            conn.close()

    def buscar_habitacion(self):
        criterio = self.numero_entry.get()
        if not criterio:
            messagebox.showwarning("Error", "Ingrese un número de habitación para buscar")
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        conn = get_connection(); cursor = conn.cursor()
        try:
            cursor.execute("SELECT numero, piso, tipo, orientacion, estado, tarifa_base, hotel_codigo FROM habitaciones WHERE numero=%s", (criterio,))
            rows = cursor.fetchall()
            if not rows:
                messagebox.showinfo("Resultado", f"No se encontró habitación con número {criterio}")
                return
            for i, row in enumerate(rows):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo buscar la habitación: {e}")
        finally:
            conn.close()
