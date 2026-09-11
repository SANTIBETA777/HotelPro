# servicio.py

class Servicio:
    def __init__(self, codigo, nombre, descripcion, horario, precio,
                    duracion, capacidad_maxima):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.horario = horario  # ejemplo: {"inicio": "08:00", "fin": "22:00"}
        self.precio = precio
        self.duracion = duracion  # en minutos
        self.capacidad_maxima = capacidad_maxima

    def mostrar_info(self):
        return f"{self.nombre} - {self.precio} USD ({self.horario['inicio']} a {self.horario['fin']})"


class ConsumoServicio:
    def __init__(self, cliente, habitacion, servicio: Servicio,
                    fecha_hora, cantidad, empleado, observaciones=""):
        self.cliente = cliente
        self.habitacion = habitacion
        self.servicio = servicio
        self.fecha_hora = fecha_hora
        self.cantidad = cantidad
        self.empleado = empleado
        self.observaciones = observaciones

    def calcular_total(self):
        return self.servicio.precio * self.cantidad

    def mostrar_info(self):
        return (f"Consumo de {self.servicio.nombre} por {self.cliente.nombres} "
                f"({self.cantidad} unidades) - Total: {self.calcular_total()} USD")
