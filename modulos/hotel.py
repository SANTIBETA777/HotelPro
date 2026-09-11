# hotel.py
class Hotel:
    def __init__(self, codigo, nombre, categoria, direccion, telefono, correo,
                    anio_inauguracion, num_habitaciones, servicios, horarios, gerente):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria  # número de estrellas
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.anio_inauguracion = anio_inauguracion
        self.num_habitaciones = num_habitaciones
        self.servicios = servicios  # lista de servicios disponibles
        self.horarios = horarios    # dict con check-in y check-out
        self.gerente = gerente

    def mostrar_info(self):
        return f"{self.nombre} ({self.categoria}★) - {self.direccion}"

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

    def actualizar_gerente(self, nuevo_gerente):
        self.gerente = nuevo_gerente
