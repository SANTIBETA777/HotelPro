# tarifa.py

class Temporada:
    def __init__(self, codigo, nombre, fecha_inicio, fecha_fin, factor):
        self.codigo = codigo
        self.nombre = nombre  # alta, media, baja
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.factor = factor  # multiplicador de tarifa

    def mostrar_info(self):
        return f"Temporada {self.nombre} ({self.fecha_inicio} - {self.fecha_fin})"


class Tarifa:
    def __init__(self, codigo, tipo_habitacion, temporada: Temporada,
                    tarifa_base, impuestos=0.0, descuento=0.0, condiciones=None):
        self.codigo = codigo
        self.tipo_habitacion = tipo_habitacion
        self.temporada = temporada
        self.tarifa_base = tarifa_base
        self.impuestos = impuestos
        self.descuento = descuento
        self.condiciones = condiciones if condiciones else []

    def calcular_precio(self, noches=1, descuento_extra=0.0, impuestos_extra=0.0):
        """Calcula el precio total aplicando temporada, impuestos y descuentos del negocio."""
        subtotal = self.tarifa_base * self.temporada.factor * noches
        descuento_total = min(max(self.descuento + descuento_extra, 0.0), 0.35)
        subtotal *= (1 - descuento_total)
        subtotal *= (1 + max(self.impuestos + impuestos_extra, 0.0))
        return round(subtotal, 2)

    def mostrar_info(self):
        return (f"Tarifa {self.codigo} - {self.tipo_habitacion} "
                f"({self.temporada.nombre}) Base: {self.tarifa_base}")
