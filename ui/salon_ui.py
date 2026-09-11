import tkinter as tk
from tkinter import ttk, messagebox
from modulos.salon import registrar_salon, obtener_salones, actualizar_salon, eliminar_salon, buscar_salon
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


class SalonUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        aplicar_estilos(parent)

        ttk.Label(self, text="Gestión de Salones", style="Titulo.TLabel").pack(pady=10)

        # ------------------ Formulario desplazable ------------------
        scroll_form = ScrollFrame(self)
        scroll_form.pack(pady=10, fill="x", padx=8)

        form_frame = scroll_form.interior

        # Campos
        self.codigo_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Código:",self.codigo_entry,"Identificador único del salón",0)
        self.nombre_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Nombre:",self.nombre_entry,"Nombre del salón",1)
        self.ubicacion_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Ubicación:",self.ubicacion_entry,"Lugar dentro del hotel",2)
        self.capacidad_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Capacidad:",self.capacidad_entry,"Número máximo de personas",3)
        self.tamano_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Tamaño (m²):",self.tamano_entry,"Área total en metros cuadrados",4)
        self.config_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Configuraciones:",self.config_entry,"Conferencia, banquete, etc.",5)
        self.tarifa_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Tarifa:",self.tarifa_entry,"Precio de alquiler",6)

        # Botones
        ttk.Button(form_frame,text="✔️ Registrar Salón",command=self.agregar_salon,style="Registrar.TButton").grid(row=7,column=0,padx=5,pady=10)
        ttk.Button(form_frame,text="✏️ Editar Salón",command=self.editar_salon,style="Editar.TButton").grid(row=7,column=1,padx=5,pady=10)
        ttk.Button(form_frame,text="🔍 Buscar Salón",command=self.buscar_salon,style="Buscar.TButton").grid(row=7,column=2,padx=5,pady=10)
        ttk.Button(form_frame,text="❌ Eliminar Salón",command=self.eliminar_salon,style="Eliminar.TButton").grid(row=7,column=3,padx=5,pady=10)

        # ------------------ Tabla con scroll vertical y horizontal ------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10, padx=8)

        columns = ("codigo","nombre","ubicacion","capacidad","tamano","configuraciones","tarifa")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())

        # Anchos iniciales razonables
        self.tree.column("codigo", width=120, anchor="w")
        self.tree.column("nombre", width=200, anchor="w")
        self.tree.column("ubicacion", width=180, anchor="w")
        self.tree.column("capacidad", width=100, anchor="center")
        self.tree.column("tamano", width=100, anchor="center")
        self.tree.column("configuraciones", width=180, anchor="w")
        self.tree.column("tarifa", width=120, anchor="e")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Layout con grid para que scrollbars y treeview se ajusten
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.tag_configure("oddrow",background="#ffffff")
        self.tree.tag_configure("evenrow",background="#d9edf7")

        def on_motion(event):
            row_id=self.tree.identify_row(event.y)
            self.tree.tag_configure("hover",background="#ffe680")
            for item in self.tree.get_children():
                self.tree.item(item,tags=())
            if row_id:
                self.tree.item(row_id,tags=("hover",))
        self.tree.bind("<Motion>",on_motion)

        # Soporte scroll horizontal con Shift + rueda del ratón
        def _on_shift_mousewheel(event):
            self.tree.xview_scroll(int(-1 * (event.delta / 120)), "units")
        self.tree.bind_all("<Shift-MouseWheel>", _on_shift_mousewheel)

        # Cargar salones desde el módulo
        self.cargar_salones()

    def _add_field(self,frame,label,entry,tip,row):
        ttk.Label(frame,text=label,style="Campo.TLabel").grid(row=row,column=0,sticky="w",pady=3)
        entry.grid(row=row,column=1,pady=3)
        Tooltip(entry,tip)

    # CRUD
    def agregar_salon(self):
        try:
            registrar_salon(
                self.codigo_entry.get(),
                self.nombre_entry.get(),
                self.ubicacion_entry.get(),
                int(self.capacidad_entry.get()) if self.capacidad_entry.get() else 0,
                float(self.tamano_entry.get()) if self.tamano_entry.get() else 0,
                self.config_entry.get(),
                float(self.tarifa_entry.get()) if self.tarifa_entry.get() else 0
            )
            tag="evenrow" if len(self.tree.get_children())%2==0 else "oddrow"
            self.tree.insert("", "end", values=(
                self.codigo_entry.get(), self.nombre_entry.get(), self.ubicacion_entry.get(),
                self.capacidad_entry.get(), self.tamano_entry.get(), self.config_entry.get(), self.tarifa_entry.get()
            ), tags=(tag,))
            # desplazar y seleccionar la última fila
            children = self.tree.get_children()
            if children:
                last = children[-1]
                self.tree.see(last)
                self.tree.selection_set(last)
            messagebox.showinfo("Éxito",f"Salón {self.codigo_entry.get()} registrado")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo registrar: {e}")

    def cargar_salones(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        try:
            for i,row in enumerate(obtener_salones()):
                tag="evenrow" if i%2==0 else "oddrow"
                self.tree.insert("", "end", values=row,tags=(tag,))
            # Opcional: desplazar al primer elemento para estabilidad
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo cargar salones: {e}")

    def editar_salon(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("Error","Seleccione un salón"); return
        codigo=self.tree.item(sel[0],"values")[0]
        try:
            actualizar_salon(
                codigo,
                self.nombre_entry.get(),
                self.ubicacion_entry.get(),
                int(self.capacidad_entry.get()) if self.capacidad_entry.get() else 0,
                float(self.tamano_entry.get()) if self.tamano_entry.get() else 0,
                self.config_entry.get(),
                float(self.tarifa_entry.get()) if self.tarifa_entry.get() else 0
            )
            self.cargar_salones()
            # asegurar que el elemento editado sea visible
            children = self.tree.get_children()
            for ch in children:
                vals = self.tree.item(ch, "values")
                if vals and vals[0] == codigo:
                    self.tree.see(ch)
                    self.tree.selection_set(ch)
                    break
            messagebox.showinfo("Éxito",f"Salón {codigo} actualizado")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo actualizar: {e}")

    def eliminar_salon(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("Error","Seleccione un salón"); return
        codigo=self.tree.item(sel[0],"values")[0]
        try:
            eliminar_salon(codigo)
            self.cargar_salones()
            messagebox.showinfo("Éxito",f"Salón {codigo} eliminado")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo eliminar: {e}")

    def buscar_salon(self):
        criterio=self.codigo_entry.get()
        if not criterio: messagebox.showwarning("Error","Ingrese un código"); return
        for row in self.tree.get_children(): self.tree.delete(row)
        try:
            resultados=buscar_salon(criterio)
            for i,row in enumerate(resultados):
                tag="evenrow" if i%2==0 else "oddrow"
                self.tree.insert("", "end", values=row,tags=(tag,))
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo buscar: {e}")
