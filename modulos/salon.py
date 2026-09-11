from database import get_connection

def registrar_salon(codigo, nombre, ubicacion, capacidad, tamano, configuraciones, tarifa):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO salones (codigo, nombre, ubicacion, capacidad, tamano, configuraciones, tarifa)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (codigo, nombre, ubicacion, capacidad, tamano, configuraciones, tarifa))
    conn.commit()
    conn.close()

def obtener_salones():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, nombre, ubicacion, capacidad, tamano, configuraciones, tarifa FROM salones")
    rows = cursor.fetchall()
    conn.close()
    return rows

def actualizar_salon(codigo, nombre, ubicacion, capacidad, tamano, configuraciones, tarifa):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE salones
        SET nombre=%s, ubicacion=%s, capacidad=%s, tamano=%s, configuraciones=%s, tarifa=%s
        WHERE codigo=%s
    """, (nombre, ubicacion, capacidad, tamano, configuraciones, tarifa, codigo))
    conn.commit()
    conn.close()

def eliminar_salon(codigo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM salones WHERE codigo=%s", (codigo,))
    conn.commit()
    conn.close()

def buscar_salon(codigo):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT codigo, nombre, ubicacion, capacidad, tamano, configuraciones, tarifa
        FROM salones WHERE codigo=%s
    """, (codigo,))
    rows = cursor.fetchall()
    conn.close()
    return rows
