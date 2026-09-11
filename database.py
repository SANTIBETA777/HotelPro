import mysql.connector

# Conexión a MySQL (WampServer + HeidiSQL)
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",       # vacío si no configuraste contraseña
        database="hotelpro"
    )

# -------------------------------
# FUNCIONES DE HOTELES
# -------------------------------
def insertar_hotel(codigo, nombre, categoria, direccion, telefono, correo, anio_inauguracion, num_habitaciones, gerente):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("InsertarHotel", (codigo, nombre, categoria, direccion, telefono, correo, anio_inauguracion, num_habitaciones, gerente))
    conn.commit()
    conn.close()

def obtener_hoteles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hoteles")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# -------------------------------
# FUNCIONES DE HABITACIONES
# -------------------------------
def insertar_habitacion(numero, piso, tipo, orientacion, estado, tarifa_base, hotel_codigo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("InsertarHabitacion", (numero, piso, tipo, orientacion, estado, tarifa_base, hotel_codigo))
    conn.commit()
    conn.close()

def obtener_habitaciones():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habitaciones")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# -------------------------------
# FUNCIONES DE CLIENTES
# -------------------------------
def insertar_cliente(id, nombres, apellidos, documento, nacionalidad, fecha_nacimiento, direccion, telefono, correo, nivel_fidelizacion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("InsertarCliente", (id, nombres, apellidos, documento, nacionalidad, fecha_nacimiento, direccion, telefono, correo, nivel_fidelizacion))
    conn.commit()
    conn.close()

def obtener_clientes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# -------------------------------
# FUNCIONES DE RESERVAS
# -------------------------------
def insertar_reserva(numero, cliente_id, fecha_creacion, fecha_llegada, fecha_salida, noches, habitaciones, tipo_habitacion, adultos, ninos, tarifa, deposito, metodo_pago, estado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("InsertarReserva", (numero, cliente_id, fecha_creacion, fecha_llegada, fecha_salida, noches, habitaciones, tipo_habitacion, adultos, ninos, tarifa, deposito, metodo_pago, estado))
    conn.commit()
    conn.close()

def obtener_reservas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservas")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# -------------------------------
# FUNCIONES DE MOVIMIENTOS (Check-In / Check-Out)
# -------------------------------
def registrar_checkin(reserva_numero, habitacion_numero, fecha_hora, empleado, observaciones):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("RegistrarCheckIn", (reserva_numero, habitacion_numero, fecha_hora, empleado, observaciones))
    conn.commit()
    conn.close()

def registrar_checkout(reserva_numero, habitacion_numero, fecha_hora, empleado, observaciones):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("RegistrarCheckOut", (reserva_numero, habitacion_numero, fecha_hora, empleado, observaciones))
    conn.commit()
    conn.close()

# -------------------------------
# FUNCIONES DE TARIFAS
# -------------------------------
def insertar_tarifa(codigo, tipo_habitacion, temporada, tarifa_base, impuestos, descuento, precio_final):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("InsertarTarifa", (codigo, tipo_habitacion, temporada, tarifa_base, impuestos, descuento, precio_final))
    conn.commit()
    conn.close()

def obtener_tarifas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarifas")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# -------------------------------
# FUNCIONES DE SERVICIOS
# -------------------------------
def insertar_servicio(codigo, nombre, descripcion, horario, precio):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("InsertarServicio", (codigo, nombre, descripcion, horario, precio))
    conn.commit()
    conn.close()

def obtener_servicios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servicios")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# -------------------------------
# FUNCIONES DE CONSUMOS
# -------------------------------
def insertar_consumo(cliente_id, habitacion_numero, servicio_codigo, fecha, cantidad, total, empleado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("InsertarConsumo", (cliente_id, habitacion_numero, servicio_codigo, fecha, cantidad, total, empleado))
    conn.commit()
    conn.close()

def obtener_consumos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consumos")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# -------------------------------
# FUNCIONES DE EVENTOS
# -------------------------------
def insertar_evento(codigo, tipo, cliente_id, fecha, duracion, asistentes, precio_total, estado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("InsertarEvento", (codigo, tipo, cliente_id, fecha, duracion, asistentes, precio_total, estado))
    conn.commit()
    conn.close()

def obtener_eventos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eventos")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# -------------------------------
# FUNCIONES DE SALONES
# -------------------------------
def insertar_salon(codigo, nombre, ubicacion, capacidad, tamano, configuraciones, tarifa):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.callproc("InsertarSalon", (codigo, nombre, ubicacion, capacidad, tamano, configuraciones, tarifa))
    conn.commit()
    conn.close()

def obtener_salones():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM salones")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# -------------------------------
# FUNCIÓN DE INICIALIZACIÓN DE BD
# -------------------------------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Ejemplo: crear tabla clientes si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id VARCHAR(50) PRIMARY KEY,
            nombres VARCHAR(100),
            apellidos VARCHAR(100),
            documento VARCHAR(50),
            nacionalidad VARCHAR(50),
            fecha_nacimiento DATE,
            direccion VARCHAR(200),
            telefono VARCHAR(20),
            correo VARCHAR(100),
            nivel_fidelizacion INT DEFAULT 0
        )
    """)

        # Crear tabla consumos si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consumos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id VARCHAR(50),
            habitacion_numero VARCHAR(50),
            servicio_codigo VARCHAR(50),
            fecha DATE,
            cantidad INT,
            total DECIMAL(10,2),
            empleado VARCHAR(100),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            FOREIGN KEY (habitacion_numero) REFERENCES habitaciones(numero),
            FOREIGN KEY (servicio_codigo) REFERENCES servicios(codigo)
        )
    """)

    # Crear tabla hoteles si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hoteles (
            codigo VARCHAR(50) PRIMARY KEY,
            nombre VARCHAR(100),
            categoria INT,
            direccion VARCHAR(200),
            telefono VARCHAR(20),
            correo VARCHAR(100),
            anio_inauguracion INT,
            num_habitaciones INT,
            gerente VARCHAR(100)
        )
    """)

    # Crear tabla habitaciones si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habitaciones (
            numero VARCHAR(50) PRIMARY KEY,
            piso INT,
            tipo VARCHAR(50),
            orientacion VARCHAR(50),
            estado VARCHAR(50),
            tarifa_base DECIMAL(10,2),
            hotel_codigo VARCHAR(50),
            FOREIGN KEY (hotel_codigo) REFERENCES hoteles(codigo)
        )
    """)

    # Crear tabla reservas si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            numero VARCHAR(50) PRIMARY KEY,
            cliente_id VARCHAR(50),
            fecha_creacion DATE,
            fecha_llegada DATE,
            fecha_salida DATE,
            noches INT,
            habitaciones INT,
            tipo_habitacion VARCHAR(50),
            adultos INT,
            ninos INT,
            tarifa DECIMAL(10,2),
            deposito DECIMAL(10,2),
            metodo_pago VARCHAR(50),
            estado VARCHAR(50),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    # Crear tabla tarifas si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarifas (
            codigo VARCHAR(50) PRIMARY KEY,
            tipo_habitacion VARCHAR(50),
            temporada VARCHAR(50),
            tarifa_base DECIMAL(10,2),
            impuestos DECIMAL(10,2),
            descuento DECIMAL(10,2),
            precio_final DECIMAL(10,2)
        )
    """)

    # Crear tabla servicios si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicios (
            codigo VARCHAR(50) PRIMARY KEY,
            nombre VARCHAR(100),
            descripcion VARCHAR(200),
            horario VARCHAR(50),
            precio DECIMAL(10,2)
        )
    """)

    # Crear tabla eventos si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eventos (
            codigo VARCHAR(50) PRIMARY KEY,
            tipo VARCHAR(50),
            cliente_id VARCHAR(50),
            fecha DATE,
            duracion INT,
            asistentes INT,
            precio_total DECIMAL(10,2),
            estado VARCHAR(50),
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    # Crear tabla salones si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS salones (
            codigo VARCHAR(50) PRIMARY KEY,
            nombre VARCHAR(100),
            ubicacion VARCHAR(100),
            capacidad INT,
            tamano DECIMAL(10,2),
            configuraciones VARCHAR(200),
            tarifa DECIMAL(10,2)
        )
    """)


    # Aquí puedes añadir más CREATE TABLE IF NOT EXISTS para hoteles, reservas, etc.

    conn.commit()
    conn.close()
