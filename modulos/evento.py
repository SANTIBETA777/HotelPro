# evento.py

class Salon:
    def __init__(self, codigo, nombre, ubicacion, capacidad_maxima,
                    metros_cuadrados, configuraciones, tarifas):
        self.codigo = codigo
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.capacidad_maxima = capacidad_maxima
        self.metros_cuadrados = metros_cuadrados
        self.configuraciones = configuraciones  # lista de posibles montajes
        self.tarifas = tarifas  # dict con tarifas según duración

    def mostrar_info(self):
        return f"Salón {self.nombre} - Capacidad: {self.capacidad_maxima} personas"


class Evento:
    def __init__(self, codigo, tipo, cliente, fecha_inicio, duracion,
                    asistentes, catering, equipamiento, montaje,
                    precio_total, estado="pendiente"):
        self.codigo = codigo
        self.tipo = tipo  # conferencia, boda, reunión
        self.cliente = cliente
        self.fecha_inicio = fecha_inicio
        self.duracion = duracion  # en horas
        self.asistentes = asistentes
        self.catering = catering  # lista de servicios de catering
        self.equipamiento = equipamiento  # lista de equipos técnicos
        self.montaje = montaje  # tipo de montaje solicitado
        self.precio_total = precio_total
        self.estado = estado  # pendiente, confirmado, cancelado

    def confirmar(self):
        self.estado = "confirmado"

    def cancelar(self):
        self.estado = "cancelado"

    def mostrar_info(self):
        return (f"Evento {self.codigo} ({self.tipo}) - Cliente: {self.cliente.nombres} "
                f"{self.cliente.apellidos}, Estado: {self.estado}, Asistentes: {self.asistentes}")
