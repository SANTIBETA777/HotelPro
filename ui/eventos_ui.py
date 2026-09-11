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


class EventosUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        aplicar_estilos(parent)

        ttk.Label(self, text="Gestión de Eventos", style="Titulo.TLabel").pack(pady=10)

        # ------------------ Formulario desplazable ------------------
        scroll_form = ScrollFrame(self)
        scroll_form.pack(pady=10, fill="x", padx=8)

        form_frame = scroll_form.interior

        # Campos
        self.codigo_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Código:",self.codigo_entry,"Identificador único del evento",0)
        self.tipo_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Tipo Evento:",self.tipo_entry,"Ejemplo: conferencia, boda, reunión",1)
        self.cliente_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Cliente ID:",self.cliente_entry,"Identificador del cliente",2)
        self.fecha_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Fecha:",self.fecha_entry,"AAAA-MM-DD",3)
        self.duracion_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Duración (horas):",self.duracion_entry,"Duración estimada",4)
        self.asistentes_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Asistentes:",self.asistentes_entry,"Número de personas",5)
        self.precio_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Precio Total:",self.precio_entry,"Costo total",6)
        self.estado_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Estado:",self.estado_entry,"Pendiente, confirmado, cancelado",7)

        # Botones
        ttk.Button(form_frame,text="✔️ Registrar Evento",command=self.agregar_evento,style="Registrar.TButton").grid(row=8,column=0,padx=5,pady=10)
        ttk.Button(form_frame,text="✏️ Editar Evento",command=self.editar_evento,style="Editar.TButton").grid(row=8,column=1,padx=5,pady=10)
        ttk.Button(form_frame,text="🔍 Buscar Evento",command=self.buscar_evento,style="Buscar.TButton").grid(row=8,column=2,padx=5,pady=10)
        ttk.Button(form_frame,text="❌ Eliminar Evento",command=self.eliminar_evento,style="Eliminar.TButton").grid(row=8,column=3,padx=5,pady=10)

        # ------------------ Tabla con scroll vertical y horizontal ------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10, padx=8)

        self.tree = ttk.Treeview(table_frame,columns=("codigo","tipo","cliente","fecha","duracion","asistentes","precio","estado"),show="headings", selectmode="browse")
        for col in ("codigo","tipo","cliente","fecha","duracion","asistentes","precio","estado"):
            self.tree.heading(col,text=col.capitalize())

        # Anchos iniciales razonables
        self.tree.column("codigo", width=120, anchor="w")
        self.tree.column("tipo", width=140, anchor="w")
        self.tree.column("cliente", width=120, anchor="center")
        self.tree.column("fecha", width=140, anchor="center")
        self.tree.column("duracion", width=100, anchor="center")
        self.tree.column("asistentes", width=100, anchor="center")
        self.tree.column("precio", width=120, anchor="e")
        self.tree.column("estado", width=120, anchor="w")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

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

        self.cargar_eventos()

    def _add_field(self,frame,label,entry,tip,row):
        ttk.Label(frame,text=label,style="Campo.TLabel").grid(row=row,column=0,sticky="w",pady=3)
        entry.grid(row=row,column=1,pady=3)
        Tooltip(entry,tip)

    # CRUD
    def agregar_evento(self):
        codigo=self.codigo_entry.get(); tipo=self.tipo_entry.get()
        cliente_id=self.cliente_entry.get(); fecha=self.fecha_entry.get()
        duracion=self.duracion_entry.get(); asistentes=self.asistentes_entry.get()
        precio=self.precio_entry.get(); estado=self.estado_entry.get()

        if not codigo or not tipo or not cliente_id or not fecha:
            messagebox.showwarning("Error","Código, tipo, cliente y fecha son obligatorios"); return

        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO eventos (codigo,tipo,cliente_id,fecha,duracion,asistentes,precio_total,estado)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """,(codigo,tipo,cliente_id,fecha,
                 int(duracion) if duracion else 0,
                 int(asistentes) if asistentes else 0,
                 float(precio) if precio else 0,
                 estado if estado else "pendiente"))
            conn.commit()
            tag="evenrow" if len(self.tree.get_children())%2==0 else "oddrow"
            self.tree.insert("", "end", values=(codigo,tipo,cliente_id,fecha,duracion,asistentes,precio,estado),tags=(tag,))
            # desplazar y seleccionar la última fila
            children = self.tree.get_children()
            if children:
                last = children[-1]
                self.tree.see(last)
                self.tree.selection_set(last)
            messagebox.showinfo("Éxito",f"Evento {codigo} registrado")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo registrar: {e}")
        finally:
            conn.close()

    def cargar_eventos(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("SELECT codigo,tipo,cliente_id,fecha,duracion,asistentes,precio_total,estado FROM eventos")
            rows=cursor.fetchall()
            for i,row in enumerate(rows):
                tag="evenrow" if i%2==0 else "oddrow"
                self.tree.insert("", "end", values=row,tags=(tag,))
            # Opcional: desplazar al primer elemento para estabilidad
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo cargar eventos: {e}")
        finally:
            conn.close()

    def editar_evento(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("Error","Seleccione un evento"); return
        codigo=self.tree.item(sel[0],"values")[0]
        tipo=self.tipo_entry.get(); cliente_id=self.cliente_entry.get()
        fecha=self.fecha_entry.get(); duracion=self.duracion_entry.get()
        asistentes=self.asistentes_entry.get(); precio=self.precio_entry.get()
        estado=self.estado_entry.get()
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("""
                UPDATE eventos SET tipo=%s,cliente_id=%s,fecha=%s,duracion=%s,asistentes=%s,precio_total=%s,estado=%s
                WHERE codigo=%s
            """,(tipo,cliente_id,fecha,
                 int(duracion) if duracion else 0,
                 int(asistentes) if asistentes else 0,
                 float(precio) if precio else 0,
                 estado,codigo))
            conn.commit(); self.cargar_eventos()
            # asegurar que el elemento editado sea visible
            children = self.tree.get_children()
            for ch in children:
                vals = self.tree.item(ch, "values")
                if vals and vals[0] == codigo:
                    self.tree.see(ch)
                    self.tree.selection_set(ch)
                    break
            messagebox.showinfo("Éxito",f"Evento {codigo} actualizado")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo actualizar: {e}")
        finally:
            conn.close()

    def eliminar_evento(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("Error","Seleccione un evento"); return
        codigo=self.tree.item(sel[0],"values")[0]
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("DELETE FROM eventos WHERE codigo=%s",(codigo,))
            conn.commit(); self.cargar_eventos()
            messagebox.showinfo("Éxito",f"Evento {codigo} eliminado")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo eliminar: {e}")
        finally:
            conn.close()

    def buscar_evento(self):
        criterio=self.codigo_entry.get()
        if not criterio: messagebox.showwarning("Error","Ingrese un código de evento"); return
        for row in self.tree.get_children(): self.tree.delete(row)
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("SELECT codigo,tipo,cliente_id,fecha,duracion,asistentes,precio_total,estado FROM eventos WHERE codigo=%s",(criterio,))
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
