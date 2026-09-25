# cliente.py

class Cliente:
    def __init__(self, id_cliente, nombres, apellidos, documento, nacionalidad,
                    fecha_nacimiento, direccion, telefono, correo,
                    preferencias=None, nivel_fidelizacion=0):
        self.id_cliente = id_cliente
        self.nombres = nombres
        self.apellidos = apellidos
        self.documento = documento
        self.nacionalidad = nacionalidad
        self.fecha_nacimiento = fecha_nacimiento
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.preferencias = preferencias if preferencias else []
        self.nivel_fidelizacion = nivel_fidelizacion  # puntos o nivel del programa

    def mostrar_info(self):
        return f"{self.nombres} {self.apellidos} - {self.correo}"

    def actualizar_contacto(self, nuevo_telefono, nuevo_correo):
        self.telefono = nuevo_telefono
        self.correo = nuevo_correo

    def agregar_preferencia(self, preferencia):
        self.preferencias.append(preferencia)

    def actualizar_fidelizacion(self, puntos):
        self.nivel_fidelizacion += puntos

    def descuento_por_fidelizacion(self):
        """Descuento según nivel de fidelización del cliente."""
        descuentos = {
            0: 0.00,
            1: 0.05,
            2: 0.10,
            3: 0.15,
            4: 0.20,
        }
        return descuentos.get(self.nivel_fidelizacion, 0.20)

    def aplicar_descuento(self, subtotal, descuento_extra=0.0):
        """Aplica descuento por fidelización + descuento adicional."""
        descuento_total = self.descuento_por_fidelizacion() + descuento_extra
        descuento_total = min(descuento_total, 0.35)
        return round(subtotal * descuento_total, 2)

    def calcular_total_con_descuento(self, subtotal, descuento_extra=0.0):
        descuento = self.aplicar_descuento(subtotal, descuento_extra)
        return round(subtotal - descuento, 2), round(descuento, 2)