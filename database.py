import mysql.connector

# Conexión a MySQL (WampServer + HeidiSQL)
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",       # vacío si no configuraste contraseña
        database="hotelpro"
    )


def ejecutar_procedimiento(nombre, parametros=()):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.callproc(nombre, tuple(parametros))
        conn.commit()
    finally:
        conn.close()


def ejecutar_crud(nombre, parametros, sql_fallback, parametros_fallback=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.callproc(nombre, tuple(parametros))
        except mysql.connector.Error:
            cursor.execute(sql_fallback, tuple(parametros_fallback or parametros))
        conn.commit()
    finally:
        conn.close()


def actualizar_hotel(*valores):
    ejecutar_crud("ActualizarHotel", valores, """UPDATE hoteles SET nombre=%s, categoria=%s,
        direccion=%s, telefono=%s, correo=%s, anio_inauguracion=%s,
        num_habitaciones=%s, gerente=%s WHERE codigo=%s""", valores[1:] + valores[:1])


def eliminar_hotel(codigo):
    ejecutar_crud("EliminarHotel", (codigo,), "DELETE FROM hoteles WHERE codigo=%s")


def actualizar_habitacion(*valores):
    ejecutar_crud("ActualizarHabitacion", valores, """UPDATE habitaciones SET piso=%s, tipo=%s,
        orientacion=%s, estado=%s, tarifa_base=%s, hotel_codigo=%s WHERE numero=%s""", valores[1:] + valores[:1])


def eliminar_habitacion(numero):
    ejecutar_crud("EliminarHabitacion", (numero,), "DELETE FROM habitaciones WHERE numero=%s")


def actualizar_cliente(*valores):
    ejecutar_crud("ActualizarCliente", valores, """UPDATE clientes SET nombres=%s, apellidos=%s,
        documento=%s, nacionalidad=%s, fecha_nacimiento=%s, direccion=%s,
        telefono=%s, correo=%s, nivel_fidelizacion=%s WHERE id=%s""", valores[1:] + valores[:1])


def eliminar_cliente(cliente_id):
    ejecutar_crud("EliminarCliente", (cliente_id,), "DELETE FROM clientes WHERE id=%s")


def actualizar_reserva(*valores):
    ejecutar_crud("ActualizarReserva", valores, """UPDATE reservas SET cliente_id=%s,
        fecha_llegada=%s, fecha_salida=%s, noches=%s, habitaciones=%s,
        tarifa=%s WHERE numero=%s""", valores[1:] + valores[:1])


def eliminar_reserva(numero):
    ejecutar_crud("EliminarReserva", (numero,), "DELETE FROM reservas WHERE numero=%s")


def actualizar_tarifa(*valores):
    ejecutar_crud("ActualizarTarifa", valores, """UPDATE tarifas SET tipo_habitacion=%s,
        temporada=%s, tarifa_base=%s, impuestos=%s, descuento=%s,
        precio_final=%s WHERE codigo=%s""", valores[1:] + valores[:1])


def eliminar_tarifa(codigo):
    ejecutar_crud("EliminarTarifa", (codigo,), "DELETE FROM tarifas WHERE codigo=%s")


def actualizar_servicio(*valores):
    ejecutar_crud("ActualizarServicio", valores, """UPDATE servicios SET nombre=%s,
        descripcion=%s, horario=%s, precio=%s WHERE codigo=%s""", valores[1:] + valores[:1])


def eliminar_servicio(codigo):
    ejecutar_crud("EliminarServicio", (codigo,), "DELETE FROM servicios WHERE codigo=%s")


def actualizar_evento(*valores):
    ejecutar_crud("ActualizarEvento", valores, """UPDATE eventos SET tipo=%s,
        cliente_id=%s, fecha=%s, duracion=%s, asistentes=%s,
        precio_total=%s, estado=%s WHERE codigo=%s""", valores[1:] + valores[:1])


def eliminar_evento(codigo):
    ejecutar_crud("EliminarEvento", (codigo,), "DELETE FROM eventos WHERE codigo=%s")


def actualizar_salon(*valores):
    ejecutar_crud("ActualizarSalon", valores, """UPDATE salones SET nombre=%s,
        ubicacion=%s, capacidad=%s, tamano=%s, configuraciones=%s,
        tarifa=%s WHERE codigo=%s""", valores[1:] + valores[:1])


def eliminar_salon(codigo):
    ejecutar_crud("EliminarSalon", (codigo,), "DELETE FROM salones WHERE codigo=%s")


def actualizar_consumo(cliente_id, habitacion, servicio, fecha, cantidad, empleado):
    ejecutar_crud(
        "ActualizarConsumo",
        (cliente_id, habitacion, servicio, fecha, cantidad, empleado),
        """UPDATE consumos SET cantidad=%s, total=(SELECT precio FROM servicios WHERE codigo=%s) * %s,
            empleado=%s WHERE cliente_id=%s AND habitacion_numero=%s AND servicio_codigo=%s AND fecha=%s""",
        (cantidad, servicio, cantidad, empleado, cliente_id, habitacion, servicio, fecha),
    )


def eliminar_consumo(cliente_id, habitacion, servicio, fecha):
    ejecutar_crud(
        "EliminarConsumo", (cliente_id, habitacion, servicio, fecha),
        """DELETE FROM consumos WHERE cliente_id=%s AND habitacion_numero=%s
            AND servicio_codigo=%s AND fecha=%s""",
    )


def actualizar_movimiento(movimiento_id, reserva, habitacion, tipo, empleado, observaciones):
    ejecutar_crud(
        "ActualizarMovimiento",
        (movimiento_id, reserva, habitacion, tipo, empleado, observaciones),
        """UPDATE movimientos SET reserva_numero=%s, habitacion_numero=%s,
            tipo=%s, empleado=%s, observaciones=%s WHERE id=%s""",
        (reserva, habitacion, tipo, empleado, observaciones, movimiento_id),
    )


def eliminar_movimiento(movimiento_id):
    ejecutar_crud("EliminarMovimiento", (movimiento_id,), "DELETE FROM movimientos WHERE id=%s")


def guardar_imagen(tabla, clave, valor):
    tablas_validas = {"hoteles": "codigo", "clientes": "id"}
    if tabla not in tablas_validas:
        raise ValueError("Tabla de imagen no permitida")
    conn = get_connection()
    try:
        cursor = conn.cursor()
        columna_clave = tablas_validas[tabla]
        cursor.execute(
            f"UPDATE {tabla} SET imagen=%s WHERE {columna_clave}=%s",
            (valor, clave),
        )
        conn.commit()
    finally:
        conn.close()

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
            nivel_fidelizacion INT DEFAULT 0,
            imagen VARCHAR(500)
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
            gerente VARCHAR(100),
            imagen VARCHAR(500)
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

    for tabla in ("hoteles", "clientes"):
        try:
            cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN imagen VARCHAR(500)")
        except mysql.connector.Error as error:
            if error.errno not in (1060, 1061):
                raise


    # Aquí puedes añadir más CREATE TABLE IF NOT EXISTS para hoteles, reservas, etc.

    conn.commit()
    conn.close()
