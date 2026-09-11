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