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

    def calcular_total_estadia(self, tarifa_noche, noches, descuento=0.0, impuestos=0.12):
        """Lógica hotelera real: subtotal por noche, descuento y tasa de impuesto."""
        subtotal = tarifa_noche * noches
        descuento_total = min(max(descuento, 0.0), 0.35)
        total = subtotal * (1 - descuento_total)
        total *= (1 + max(impuestos, 0.0))
        return round(total, 2)

    def disponibilidad_habitaciones(self, habitaciones_disponibles):
        return sum(1 for h in habitaciones_disponibles if h.estado == "disponible")
