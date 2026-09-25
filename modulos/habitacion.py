# habitacion.py

class TipoHabitacion:
    def __init__(self, codigo, descripcion, capacidad, metros_cuadrados,
                    num_camas, tipo_camas, amenidades):
        self.codigo = codigo
        self.descripcion = descripcion  # individual, doble, suite
        self.capacidad = capacidad
        self.metros_cuadrados = metros_cuadrados
        self.num_camas = num_camas
        self.tipo_camas = tipo_camas
        self.amenidades = amenidades  # lista de strings

    def mostrar_info(self):
        return f"{self.descripcion} ({self.capacidad} huéspedes, {self.num_camas} camas)"


class Habitacion:
    def __init__(self, numero, piso, tipo: TipoHabitacion,
                    orientacion, estado, caracteristicas, tarifa_base):
        self.numero = numero
        self.piso = piso
        self.tipo = tipo  # objeto TipoHabitacion
        self.orientacion = orientacion
        self.estado = estado  # disponible, ocupada, mantenimiento
        self.caracteristicas = caracteristicas  # lista de strings
        self.tarifa_base = tarifa_base

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def calcular_tarifa(self, temporada_factor=1.0, descuento=0.0, noches=1, impuestos=0.0):
        """Calcula la tarifa total de noches aplicando temporada, impuestos y descuentos."""
        subtotal = self.tarifa_base * temporada_factor * noches
        descuento_total = min(max(descuento, 0.0), 0.35)
        subtotal *= (1 - descuento_total)
        subtotal *= (1 + max(impuestos, 0.0))
        return round(subtotal, 2)

    def mostrar_info(self):
        return f"Habitación {self.numero} ({self.tipo.descripcion}) - Estado: {self.estado}"
