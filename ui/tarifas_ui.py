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


class TarifasUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        aplicar_estilos(parent)

        ttk.Label(self, text="Gestión de Tarifas y Temporadas", style="Titulo.TLabel").pack(pady=10)

        # ------------------ Formulario desplazable ------------------
        scroll_form = ScrollFrame(self)
        scroll_form.pack(pady=10, fill="x", padx=8)

        form_frame = scroll_form.interior

        # Campos
        self.codigo_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Código Tarifa:",self.codigo_entry,"Identificador único de la tarifa",0)
        self.tipo_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Tipo Habitación:",self.tipo_entry,"Tipo de habitación",1)
        self.temporada_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Temporada:",self.temporada_entry,"Alta, baja o especial",2)
        self.base_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Tarifa Base:",self.base_entry,"Precio inicial",3)
        self.impuestos_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Impuestos (%):",self.impuestos_entry,"Porcentaje de impuestos",4)
        self.descuento_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Descuento (%):",self.descuento_entry,"Porcentaje de descuento",5)

        # Botones
        ttk.Button(form_frame,text="✔️ Registrar Tarifa",command=self.agregar_tarifa,style="Registrar.TButton").grid(row=6,column=0,padx=5,pady=10)
        ttk.Button(form_frame,text="✏️ Editar Tarifa",command=self.editar_tarifa,style="Editar.TButton").grid(row=6,column=1,padx=5,pady=10)
        ttk.Button(form_frame,text="🔍 Buscar Tarifa",command=self.buscar_tarifa,style="Buscar.TButton").grid(row=6,column=2,padx=5,pady=10)
        ttk.Button(form_frame,text="❌ Eliminar Tarifa",command=self.eliminar_tarifa,style="Eliminar.TButton").grid(row=6,column=3,padx=5,pady=10)

        # ------------------ Tabla con scroll vertical y horizontal ------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10, padx=8)

        columns = ("codigo","tipo","temporada","base","precio_final")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())

        # Anchos iniciales razonables
        self.tree.column("codigo", width=120, anchor="w")
        self.tree.column("tipo", width=160, anchor="w")
        self.tree.column("temporada", width=120, anchor="center")
        self.tree.column("base", width=100, anchor="e")
        self.tree.column("precio_final", width=120, anchor="e")

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

        self.cargar_tarifas()

    def _add_field(self,frame,label,entry,tip,row):
        ttk.Label(frame,text=label,style="Campo.TLabel").grid(row=row,column=0,sticky="w",pady=3)
        entry.grid(row=row,column=1,pady=3)
        Tooltip(entry,tip)

    # CRUD
    def agregar_tarifa(self):
        try:
            base_val=float(self.base_entry.get())
            impuestos_val=float(self.impuestos_entry.get())/100 if self.impuestos_entry.get() else 0
            descuento_val=float(self.descuento_entry.get())/100 if self.descuento_entry.get() else 0
            precio_final=base_val*(1+impuestos_val)*(1-descuento_val)
        except ValueError:
            messagebox.showerror("Error","Valores numéricos inválidos"); return

        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO tarifas (codigo,tipo_habitacion,temporada,tarifa_base,impuestos,descuento,precio_final)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,(self.codigo_entry.get(),self.tipo_entry.get(),self.temporada_entry.get(),
                 base_val,impuestos_val,descuento_val,precio_final))
            conn.commit()
            tag="evenrow" if len(self.tree.get_children())%2==0 else "oddrow"
            self.tree.insert("", "end", values=(self.codigo_entry.get(),self.tipo_entry.get(),
                                                self.temporada_entry.get(),base_val,precio_final),tags=(tag,))
            # desplazar y seleccionar la última fila
            children = self.tree.get_children()
            if children:
                last = children[-1]
                self.tree.see(last)
                self.tree.selection_set(last)
            messagebox.showinfo("Éxito",f"Tarifa {self.codigo_entry.get()} registrada")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo registrar: {e}")
        finally:
            conn.close()

    def cargar_tarifas(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("SELECT codigo,tipo_habitacion,temporada,tarifa_base,precio_final FROM tarifas")
            rows=cursor.fetchall()
            for i,row in enumerate(rows):
                tag="evenrow" if i%2==0 else "oddrow"
                self.tree.insert("", "end", values=row,tags=(tag,))
            # Opcional: desplazar al primer elemento para estabilidad
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo cargar tarifas: {e}")
        finally:
            conn.close()

    def editar_tarifa(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("Error","Seleccione una tarifa"); return
        codigo=self.tree.item(sel[0],"values")[0]
        try:
            base_val=float(self.base_entry.get())
            impuestos_val=float(self.impuestos_entry.get())/100 if self.impuestos_entry.get() else 0
            descuento_val=float(self.descuento_entry.get())/100 if self.descuento_entry.get() else 0
            precio_final=base_val*(1+impuestos_val)*(1-descuento_val)
        except ValueError:
            messagebox.showerror("Error","Valores numéricos inválidos"); return

        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("""
                UPDATE tarifas SET tipo_habitacion=%s,temporada=%s,tarifa_base=%s,
                    impuestos=%s,descuento=%s,precio_final=%s WHERE codigo=%s
            """,(self.tipo_entry.get(),self.temporada_entry.get(),base_val,
                 impuestos_val,descuento_val,precio_final,codigo))
            conn.commit(); self.cargar_tarifas()
            # asegurar que el elemento editado sea visible
            children = self.tree.get_children()
            for ch in children:
                vals = self.tree.item(ch, "values")
                if vals and vals[0] == codigo:
                    self.tree.see(ch)
                    self.tree.selection_set(ch)
                    break
            messagebox.showinfo("Éxito",f"Tarifa {codigo} actualizada")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo actualizar: {e}")
        finally:
            conn.close()

    def eliminar_tarifa(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("Error","Seleccione una tarifa"); return
        codigo=self.tree.item(sel[0],"values")[0]
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("DELETE FROM tarifas WHERE codigo=%s",(codigo,))
            conn.commit(); self.cargar_tarifas()
            messagebox.showinfo("Éxito",f"Tarifa {codigo} eliminada")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo eliminar: {e}")
        finally:
            conn.close()

    def buscar_tarifa(self):
        criterio=self.codigo_entry.get()
        if not criterio: messagebox.showwarning("Error","Ingrese un código de tarifa"); return
        for row in self.tree.get_children(): self.tree.delete(row)
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("SELECT codigo,tipo_habitacion,temporada,tarifa_base,precio_final FROM tarifas WHERE codigo=%s",(criterio,))
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
