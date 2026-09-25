import mysql.connector
from database import actualizar_consumo as actualizar_consumo_proc
from database import eliminar_consumo as eliminar_consumo_proc
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

    cursor.callproc("InsertarConsumo", (
        cliente_id, habitacion_numero, servicio_codigo,
        fecha, cantidad, total, empleado
    ))

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
    actualizar_consumo_proc(cliente_id, habitacion_numero, servicio_codigo, fecha, cantidad, empleado)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT total FROM consumos WHERE cliente_id=%s AND habitacion_numero=%s AND servicio_codigo=%s AND fecha=%s",
                   (cliente_id, habitacion_numero, servicio_codigo, fecha))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else 0


def eliminar_consumo(cliente_id, habitacion_numero, servicio_codigo, fecha):
    eliminar_consumo_proc(cliente_id, habitacion_numero, servicio_codigo, fecha)


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
