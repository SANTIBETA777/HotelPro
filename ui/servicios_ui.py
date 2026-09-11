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


class ServiciosUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        aplicar_estilos(parent)

        ttk.Label(self, text="Gestión de Servicios", style="Titulo.TLabel").pack(pady=10)

        # ------------------ Formulario desplazable ------------------
        scroll_form = ScrollFrame(self)
        scroll_form.pack(pady=10, fill="x", padx=8)

        form_frame = scroll_form.interior

        # Campos
        self.codigo_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Código:",self.codigo_entry,"Identificador único del servicio",0)
        self.nombre_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Nombre:",self.nombre_entry,"Nombre del servicio",1)
        self.descripcion_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Descripción:",self.descripcion_entry,"Detalle del servicio",2)
        self.horario_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Horario:",self.horario_entry,"Disponibilidad (ej. 8am-10pm)",3)
        self.precio_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Precio:",self.precio_entry,"Costo unitario",4)

        # Botones
        ttk.Button(form_frame,text="✔️ Registrar Servicio",command=self.agregar_servicio,style="Registrar.TButton").grid(row=5,column=0,padx=5,pady=10)
        ttk.Button(form_frame,text="✏️ Editar Servicio",command=self.editar_servicio,style="Editar.TButton").grid(row=5,column=1,padx=5,pady=10)
        ttk.Button(form_frame,text="🔍 Buscar Servicio",command=self.buscar_servicio,style="Buscar.TButton").grid(row=5,column=2,padx=5,pady=10)
        ttk.Button(form_frame,text="❌ Eliminar Servicio",command=self.eliminar_servicio,style="Eliminar.TButton").grid(row=5,column=3,padx=5,pady=10)

        # ------------------ Tabla con scroll vertical y horizontal ------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10, padx=8)

        columns = ("codigo","nombre","descripcion","horario","precio")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())

        # Anchos iniciales razonables
        self.tree.column("codigo", width=120, anchor="w")
        self.tree.column("nombre", width=200, anchor="w")
        self.tree.column("descripcion", width=300, anchor="w")
        self.tree.column("horario", width=160, anchor="center")
        self.tree.column("precio", width=100, anchor="e")

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

        self.cargar_servicios()

    def _add_field(self,frame,label,entry,tip,row):
        ttk.Label(frame,text=label,style="Campo.TLabel").grid(row=row,column=0,sticky="w",pady=3)
        entry.grid(row=row,column=1,pady=3)
        Tooltip(entry,tip)

    # CRUD
    def agregar_servicio(self):
        codigo=self.codigo_entry.get(); nombre=self.nombre_entry.get()
        descripcion=self.descripcion_entry.get(); horario=self.horario_entry.get()
        precio=self.precio_entry.get()

        if not codigo or not nombre or not precio:
            messagebox.showwarning("Error","Código, nombre y precio son obligatorios"); return

        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("INSERT INTO servicios (codigo,nombre,descripcion,horario,precio) VALUES (%s,%s,%s,%s,%s)",
                           (codigo,nombre,descripcion,horario,float(precio)))
            conn.commit()
            tag="evenrow" if len(self.tree.get_children())%2==0 else "oddrow"
            self.tree.insert("", "end", values=(codigo,nombre,descripcion,horario,precio),tags=(tag,))
            # desplazar y seleccionar la última fila
            children = self.tree.get_children()
            if children:
                last = children[-1]
                self.tree.see(last)
                self.tree.selection_set(last)
            messagebox.showinfo("Éxito",f"Servicio {nombre} registrado")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo registrar: {e}")
        finally:
            conn.close()

    def cargar_servicios(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("SELECT codigo,nombre,descripcion,horario,precio FROM servicios")
            rows=cursor.fetchall()
            for i,row in enumerate(rows):
                tag="evenrow" if i%2==0 else "oddrow"
                self.tree.insert("", "end", values=row,tags=(tag,))
            # Opcional: desplazar al primer elemento para estabilidad
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo cargar servicios: {e}")
        finally:
            conn.close()

    def editar_servicio(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("Error","Seleccione un servicio"); return
        codigo=self.tree.item(sel[0],"values")[0]
        nombre=self.nombre_entry.get(); descripcion=self.descripcion_entry.get()
        horario=self.horario_entry.get(); precio=self.precio_entry.get()
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("""
                UPDATE servicios SET nombre=%s,descripcion=%s,horario=%s,precio=%s WHERE codigo=%s
            """,(nombre,descripcion,horario,float(precio) if precio else 0,codigo))
            conn.commit(); self.cargar_servicios()
            # asegurar que el elemento editado sea visible
            children = self.tree.get_children()
            for ch in children:
                vals = self.tree.item(ch, "values")
                if vals and vals[0] == codigo:
                    self.tree.see(ch)
                    self.tree.selection_set(ch)
                    break
            messagebox.showinfo("Éxito",f"Servicio {codigo} actualizado")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo actualizar: {e}")
        finally:
            conn.close()

    def eliminar_servicio(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("Error","Seleccione un servicio"); return
        codigo=self.tree.item(sel[0],"values")[0]
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("DELETE FROM servicios WHERE codigo=%s",(codigo,))
            conn.commit(); self.cargar_servicios()
            messagebox.showinfo("Éxito",f"Servicio {codigo} eliminado")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo eliminar: {e}")
        finally:
            conn.close()

    def buscar_servicio(self):
        criterio=self.codigo_entry.get()
        if not criterio: messagebox.showwarning("Error","Ingrese un código de servicio"); return
        for row in self.tree.get_children(): self.tree.delete(row)
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("SELECT codigo,nombre,descripcion,horario,precio FROM servicios WHERE codigo=%s",(criterio,))
            rows=cursor.fetchall()
            for i,row in enumerate(rows):
                tag="evenrow" if i%2==0 else "oddrow"
                self.tree.insert("", "end", values=row,tags=(tag,))
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo buscar: {e}")
        finally:
            conn.close()
