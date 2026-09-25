# reserva.py

from modulos.cliente import Cliente
from modulos.habitacion import Habitacion

class Reserva:
    def __init__(self, numero_reserva, cliente: Cliente, fecha_creacion,
                    fecha_llegada, fecha_salida, num_noches, num_habitaciones,
                    tipo_habitacion, num_adultos, num_ninos,
                    tarifa_aplicada, deposito, metodo_pago,
                    solicitudes_especiales=None, estado="confirmada"):
        self.numero_reserva = numero_reserva
        self.cliente = cliente
        self.fecha_creacion = fecha_creacion
        self.fecha_llegada = fecha_llegada
        self.fecha_salida = fecha_salida
        self.num_noches = num_noches
        self.num_habitaciones = num_habitaciones
        self.tipo_habitacion = tipo_habitacion
        self.num_adultos = num_adultos
        self.num_ninos = num_ninos
        self.tarifa_aplicada = tarifa_aplicada
        self.deposito = deposito
        self.metodo_pago = metodo_pago
        self.solicitudes_especiales = solicitudes_especiales if solicitudes_especiales else []
        self.estado = estado  # confirmada, cancelada, completada

    def cancelar(self):
        self.estado = "cancelada"

    def completar(self):
        self.estado = "completada"

    def mostrar_info(self):
        return (f"Reserva {self.numero_reserva} - Cliente: {self.cliente.nombres} "
                f"{self.cliente.apellidos}, Estado: {self.estado}")

    def calcular_total(self, descuento_cliente=0.0, descuento_promocional=0.0, impuestos=0.12):
        """Calcula el total real de la reserva considerando noches, habitaciones, impuestos y descuentos."""
        subtotal = self.tarifa_aplicada * self.num_noches * self.num_habitaciones
        descuento_total = min(max(descuento_cliente + descuento_promocional, 0.0), 0.35)
        subtotal_descuento = subtotal * (1 - descuento_total)
        total = subtotal_descuento * (1 + max(impuestos, 0.0))
        return round(total, 2)

    def calcular_descuento(self, descuento_cliente=0.0, descuento_promocional=0.0):
        subtotal = self.tarifa_aplicada * self.num_noches * self.num_habitaciones
        descuento_total = min(max(descuento_cliente + descuento_promocional, 0.0), 0.35)
        return round(subtotal * descuento_total, 2)
