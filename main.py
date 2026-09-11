import tkinter as tk
from tkinter import ttk

# Importar inicialización de la base de datos
from database import init_db

# Importar las interfaces gráficas
from ui.hoteles_ui import HotelesUI
from ui.habitaciones_ui import HabitacionesUI   # <-- Nueva importación
from ui.clientes_ui import ClientesUI
from ui.reservas_ui import ReservasUI
from ui.checkin_checkout_ui import CheckInCheckOutUI
from ui.tarifas_ui import TarifasUI
from ui.servicios_ui import ServiciosUI
from ui.eventos_ui import EventosUI
from ui.consumo_ui import ConsumosUI   # <-- 👈 Importación añadida
from ui.salon_ui import SalonUI        # <-- 👈 Nueva importación
from ui.style import aplicar_estilos      # 👈 Importar estilos


class HotelProApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HotelPro - Sistema de Gestión Hotelera")
        self.geometry("900x600")

        # Aplicar estilos visuales
        aplicar_estilos(self)

        # Inicializar la base de datos (crear tablas si no existen)
        init_db()

        # Crear Notebook (pestañas)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # 📑 Orden lógico de pestañas (sin style aquí)
        notebook.add(HotelesUI(notebook), text="Hoteles")
        notebook.add(HabitacionesUI(notebook), text="Habitaciones")
        notebook.add(ClientesUI(notebook), text="Clientes")
        notebook.add(ReservasUI(notebook), text="Reservas")
        notebook.add(CheckInCheckOutUI(notebook), text="Check-In/Out")
        notebook.add(TarifasUI(notebook), text="Tarifas")
        notebook.add(ServiciosUI(notebook), text="Servicios")
        notebook.add(ConsumosUI(notebook), text="Consumos")
        notebook.add(EventosUI(notebook), text="Eventos")
        notebook.add(SalonUI(notebook), text="Salones")


if __name__ == "__main__":
    app = HotelProApp()
    app.mainloop()
