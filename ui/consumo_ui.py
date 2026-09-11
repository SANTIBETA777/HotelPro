import tkinter as tk
from tkinter import ttk, messagebox
from modulos.consumo import registrar_consumo, obtener_consumos, actualizar_consumo, eliminar_consumo, buscar_consumo
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

class ConsumosUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        aplicar_estilos(parent)

        ttk.Label(self, text="Gestión de Consumos", style="Titulo.TLabel").pack(pady=10)

        # ------------------ Formulario desplazable ------------------
        scroll_form = ScrollFrame(self)
        scroll_form.pack(pady=10, fill="x", padx=8)

        form = scroll_form.interior

        ttk.Label(form, text="Cliente ID:", style="Campo.TLabel").grid(row=0, column=0, sticky="w", pady=3)
        self.cliente_id = ttk.Entry(form); self.cliente_id.grid(row=0, column=1, pady=3)
        Tooltip(self.cliente_id, "Identificador único del cliente que realiza el consumo")

        ttk.Label(form, text="Habitación:", style="Campo.TLabel").grid(row=1, column=0, sticky="w", pady=3)
        self.habitacion = ttk.Entry(form); self.habitacion.grid(row=1, column=1, pady=3)
        Tooltip(self.habitacion, "Número de la habitación asociada al consumo")

        ttk.Label(form, text="Servicio Código:", style="Campo.TLabel").grid(row=2, column=0, sticky="w", pady=3)
        self.servicio = ttk.Entry(form); self.servicio.grid(row=2, column=1, pady=3)
        Tooltip(self.servicio, "Código del servicio consumido (ej. SPA01)")

        ttk.Label(form, text="Fecha:", style="Campo.TLabel").grid(row=3, column=0, sticky="w", pady=3)
        self.fecha = ttk.Entry(form); self.fecha.grid(row=3, column=1, pady=3)
        Tooltip(self.fecha, "Fecha del consumo en formato AAAA-MM-DD")

        ttk.Label(form, text="Cantidad:", style="Campo.TLabel").grid(row=4, column=0, sticky="w", pady=3)
        self.cantidad = ttk.Entry(form); self.cantidad.grid(row=4, column=1, pady=3)
        Tooltip(self.cantidad, "Número de unidades consumidas")

        ttk.Label(form, text="Empleado:", style="Campo.TLabel").grid(row=5, column=0, sticky="w", pady=3)
        self.empleado = ttk.Entry(form); self.empleado.grid(row=5, column=1, pady=3)
        Tooltip(self.empleado, "Nombre del empleado que registra el consumo")

        # Botones
        ttk.Button(form, text="✔️ Registrar Consumo",
                   command=self.registrar_consumo, style="Registrar.TButton").grid(row=6, column=0, padx=5, pady=10)
        ttk.Button(form, text="✏️ Editar Consumo",
                   command=self.editar_consumo, style="Editar.TButton").grid(row=6, column=1, padx=5, pady=10)
        ttk.Button(form, text="🔍 Buscar Consumo",
                   command=self.buscar_consumo, style="Buscar.TButton").grid(row=6, column=2, padx=5, pady=10)
        ttk.Button(form, text="❌ Eliminar Consumo",
                   command=self.eliminar_consumo, style="Eliminar.TButton").grid(row=6, column=3, padx=5, pady=10)

        # ------------------ Tabla con scroll vertical y horizontal ------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10, padx=8)

        columns = ("cliente", "habitacion", "servicio", "fecha", "cantidad", "total", "empleado")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())

        # Anchos iniciales razonables
        self.tree.column("cliente", width=120, anchor="w")
        self.tree.column("habitacion", width=120, anchor="w")
        self.tree.column("servicio", width=140, anchor="w")
        self.tree.column("fecha", width=120, anchor="center")
        self.tree.column("cantidad", width=90, anchor="center")
        self.tree.column("total", width=100, anchor="center")
        self.tree.column("empleado", width=160, anchor="w")

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

        # Cargar consumos desde la BD / módulo
        self.cargar_consumos()

    # Métodos CRUD
    def registrar_consumo(self):
        try:
            total = registrar_consumo(
                self.cliente_id.get(),
                self.habitacion.get(),
                self.servicio.get(),
                self.fecha.get(),
                int(self.cantidad.get()),
                self.empleado.get()
            )
            messagebox.showinfo("Éxito", f"Consumo registrado con total {total}")
            # recargar y desplazar a la última fila
            self.cargar_consumos()
            children = self.tree.get_children()
            if children:
                last = children[-1]
                self.tree.see(last)
                self.tree.selection_set(last)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar_consumos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            for i, row in enumerate(obtener_consumos()):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))
            # Opcional: desplazar al primer elemento para estabilidad
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar consumos: {e}")

    def editar_consumo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un consumo para editar")
            return
        item = self.tree.item(selected[0]); cliente_id, habitacion, servicio, fecha, cantidad, total, empleado = item["values"]
        try:
            nuevo_total = actualizar_consumo(
                cliente_id,
                habitacion,
                servicio,
                fecha,
                int(self.cantidad.get()),
                self.empleado.get()
            )
            self.cargar_consumos()
            # asegurar que el elemento editado sea visible (si existe)
            children = self.tree.get_children()
            for ch in children:
                vals = self.tree.item(ch, "values")
                if vals and vals[0] == cliente_id and vals[1] == habitacion and vals[2] == servicio:
                    self.tree.see(ch)
                    self.tree.selection_set(ch)
                    break
            messagebox.showinfo("Éxito", f"Consumo actualizado con nuevo total {nuevo_total}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_consumo(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Seleccione un consumo para eliminar")
            return
        item = self.tree.item(selected[0]); cliente_id, habitacion, servicio, fecha, cantidad, total, empleado = item["values"]
        try:
            eliminar_consumo(cliente_id, habitacion, servicio, fecha)
            self.cargar_consumos()
            messagebox.showinfo("Éxito", "Consumo eliminado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def buscar_consumo(self):
        criterio = self.cliente_id.get()
        if not criterio:
            messagebox.showwarning("Error", "Ingrese un Cliente ID para buscar")
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            resultados = buscar_consumo(criterio)
            for i, row in enumerate(resultados):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error", str(e))
