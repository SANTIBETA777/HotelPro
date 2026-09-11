import mysql.connector
from database import get_connection

def registrar_consumo(cliente_id, habitacion_numero, servicio_codigo, fecha, cantidad, empleado):
    conn = get_connection()
    cursor = conn.cursor()

    # Obtener precio del servicio
    cursor.execute("SELECT precio FROM servicios WHERE codigo=%s", (servicio_codigo,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise ValueError("Servicio no encontrado")

    precio = row[0]
    total = precio * cantidad

    cursor.execute("""
        INSERT INTO consumos (cliente_id, habitacion_numero, servicio_codigo, fecha, cantidad, total, empleado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (cliente_id, habitacion_numero, servicio_codigo, fecha, cantidad, total, empleado))

    conn.commit()
    conn.close()
    return total


def obtener_consumos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cliente_id, habitacion_numero, servicio_codigo, fecha, cantidad, total, empleado FROM consumos")
    rows = cursor.fetchall()
    conn.close()
    return rows


def actualizar_consumo(cliente_id, habitacion_numero, servicio_codigo, fecha, cantidad, empleado):
    conn = get_connection()
    cursor = conn.cursor()

    # Recalcular total
    cursor.execute("SELECT precio FROM servicios WHERE codigo=%s", (servicio_codigo,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise ValueError("Servicio no encontrado")

    precio = row[0]
    total = precio * cantidad

    cursor.execute("""
        UPDATE consumos
        SET cantidad=%s, total=%s, empleado=%s
        WHERE cliente_id=%s AND habitacion_numero=%s AND servicio_codigo=%s AND fecha=%s
    """, (cantidad, total, empleado, cliente_id, habitacion_numero, servicio_codigo, fecha))

    conn.commit()
    conn.close()
    return total


def eliminar_consumo(cliente_id, habitacion_numero, servicio_codigo, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM consumos
        WHERE cliente_id=%s AND habitacion_numero=%s AND servicio_codigo=%s AND fecha=%s
    """, (cliente_id, habitacion_numero, servicio_codigo, fecha))
    conn.commit()
    conn.close()


def buscar_consumo(cliente_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cliente_id, habitacion_numero, servicio_codigo, fecha, cantidad, total, empleado
        FROM consumos WHERE cliente_id=%s
    """, (cliente_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows
