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


class ReservasUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        aplicar_estilos(parent)

        ttk.Label(self, text="Gestión de Reservas", style="Titulo.TLabel").pack(pady=10)

        # ------------------ Formulario desplazable ------------------
        scroll_form = ScrollFrame(self)
        scroll_form.pack(pady=10, fill="x", padx=8)

        form_frame = scroll_form.interior

        # Campos
        self.numero_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Número Reserva:",self.numero_entry,0)
        self.cliente_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Cliente ID:",self.cliente_entry,1)
        self.llegada_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Fecha Llegada:",self.llegada_entry,2)
        self.salida_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Fecha Salida:",self.salida_entry,3)
        self.noches_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Noches:",self.noches_entry,4)
        self.habitaciones_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Habitaciones:",self.habitaciones_entry,5)
        self.tarifa_entry = ttk.Entry(form_frame); self._add_field(form_frame,"Tarifa:",self.tarifa_entry,6)

        # Botones
        ttk.Button(form_frame,text="✔️ Registrar Reserva",command=self.agregar_reserva,style="Registrar.TButton").grid(row=7,column=0,padx=5,pady=10)
        ttk.Button(form_frame,text="✏️ Editar Reserva",command=self.editar_reserva,style="Editar.TButton").grid(row=7,column=1,padx=5,pady=10)
        ttk.Button(form_frame,text="🔍 Buscar Reserva",command=self.buscar_reserva,style="Buscar.TButton").grid(row=7,column=2,padx=5,pady=10)
        ttk.Button(form_frame,text="❌ Eliminar Reserva",command=self.eliminar_reserva,style="Eliminar.TButton").grid(row=7,column=3,padx=5,pady=10)

        # ------------------ Tabla con scroll vertical y horizontal ------------------
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10, padx=8)

        columns = ("numero","cliente","llegada","salida","estado")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        for col in columns:
            self.tree.heading(col, text=col.capitalize())

        # Anchos iniciales razonables
        self.tree.column("numero", width=120, anchor="w")
        self.tree.column("cliente", width=140, anchor="w")
        self.tree.column("llegada", width=140, anchor="center")
        self.tree.column("salida", width=140, anchor="center")
        self.tree.column("estado", width=120, anchor="center")

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

        self.cargar_reservas()

    def _add_field(self,frame,label,entry,row):
        ttk.Label(frame,text=label,style="Campo.TLabel").grid(row=row,column=0,sticky="w",pady=3)
        entry.grid(row=row,column=1,pady=3)
        Tooltip(entry,label)

    # CRUD
    def agregar_reserva(self):
        numero=self.numero_entry.get(); cliente_id=self.cliente_entry.get()
        llegada=self.llegada_entry.get(); salida=self.salida_entry.get()
        noches=self.noches_entry.get(); habitaciones=self.habitaciones_entry.get()
        tarifa=self.tarifa_entry.get()

        if not numero or not cliente_id or not llegada or not salida:
            messagebox.showwarning("Error","Campos obligatorios vacíos"); return

        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO reservas (numero,cliente_id,fecha_creacion,fecha_llegada,fecha_salida,
                                      noches,habitaciones,tarifa,estado)
                VALUES (%s,%s,CURDATE(),%s,%s,%s,%s,%s,%s)
            """,(numero,cliente_id,llegada,salida,
                 int(noches) if noches else 1,
                 int(habitaciones) if habitaciones else 1,
                 float(tarifa) if tarifa else 0,
                 "confirmada"))
            conn.commit()
            tag="evenrow" if len(self.tree.get_children())%2==0 else "oddrow"
            self.tree.insert("", "end", values=(numero,cliente_id,llegada,salida,"confirmada"),tags=(tag,))
            # desplazar y seleccionar la última fila
            children = self.tree.get_children()
            if children:
                last = children[-1]
                self.tree.see(last)
                self.tree.selection_set(last)
            messagebox.showinfo("Éxito",f"Reserva {numero} registrada")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo registrar: {e}")
        finally:
            conn.close()

    def cargar_reservas(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("SELECT numero,cliente_id,fecha_llegada,fecha_salida,estado FROM reservas")
            rows=cursor.fetchall()
            for i,row in enumerate(rows):
                tag="evenrow" if i%2==0 else "oddrow"
                self.tree.insert("", "end", values=row,tags=(tag,))
            # Opcional: desplazar al primer elemento para estabilidad
            children = self.tree.get_children()
            if children:
                self.tree.see(children[0])
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo cargar reservas: {e}")
        finally:
            conn.close()

    def editar_reserva(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("Error","Seleccione una reserva"); return
        numero=self.tree.item(sel[0],"values")[0]
        cliente_id=self.cliente_entry.get(); llegada=self.llegada_entry.get()
        salida=self.salida_entry.get(); noches=self.noches_entry.get()
        habitaciones=self.habitaciones_entry.get(); tarifa=self.tarifa_entry.get()
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("""
                UPDATE reservas SET cliente_id=%s,fecha_llegada=%s,fecha_salida=%s,
                    noches=%s,habitaciones=%s,tarifa=%s,estado=%s WHERE numero=%s
            """,(cliente_id,llegada,salida,
                 int(noches) if noches else 1,
                 int(habitaciones) if habitaciones else 1,
                 float(tarifa) if tarifa else 0,
                 "confirmada",numero))
            conn.commit(); self.cargar_reservas()
            # asegurar que el elemento editado sea visible
            children = self.tree.get_children()
            for ch in children:
                vals = self.tree.item(ch, "values")
                if vals and vals[0] == numero:
                    self.tree.see(ch)
                    self.tree.selection_set(ch)
                    break
            messagebox.showinfo("Éxito",f"Reserva {numero} actualizada")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo actualizar: {e}")
        finally:
            conn.close()

    def eliminar_reserva(self):
        sel=self.tree.selection()
        if not sel: messagebox.showwarning("Error","Seleccione una reserva"); return
        numero=self.tree.item(sel[0],"values")[0]
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("DELETE FROM reservas WHERE numero=%s",(numero,))
            conn.commit(); self.cargar_reservas()
            messagebox.showinfo("Éxito",f"Reserva {numero} eliminada")
        except Exception as e:
            messagebox.showerror("Error",f"No se pudo eliminar: {e}")
        finally:
            conn.close()

    def buscar_reserva(self):
        criterio=self.numero_entry.get()
        if not criterio: messagebox.showwarning("Error","Ingrese un número de reserva"); return
        for row in self.tree.get_children(): self.tree.delete(row)
        conn=get_connection(); cursor=conn.cursor()
        try:
            cursor.execute("SELECT numero,cliente_id,fecha_llegada,fecha_salida,estado FROM reservas WHERE numero=%s",(criterio,))
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
