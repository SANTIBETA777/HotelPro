USE hotelpro;

DELIMITER $$

DROP PROCEDURE IF EXISTS ActualizarHotel$$
CREATE PROCEDURE ActualizarHotel(
    IN p_codigo VARCHAR(50), IN p_nombre VARCHAR(100), IN p_categoria INT,
    IN p_direccion VARCHAR(200), IN p_telefono VARCHAR(20), IN p_correo VARCHAR(100),
    IN p_anio INT, IN p_habitaciones INT, IN p_gerente VARCHAR(100)
)
BEGIN
    UPDATE hoteles SET nombre=p_nombre, categoria=p_categoria, direccion=p_direccion,
        telefono=p_telefono, correo=p_correo, anio_inauguracion=p_anio,
        num_habitaciones=p_habitaciones, gerente=p_gerente WHERE codigo=p_codigo;
END$$

DROP PROCEDURE IF EXISTS EliminarHotel$$
CREATE PROCEDURE EliminarHotel(IN p_codigo VARCHAR(50))
BEGIN DELETE FROM hoteles WHERE codigo=p_codigo; END$$

DROP PROCEDURE IF EXISTS ActualizarHabitacion$$
CREATE PROCEDURE ActualizarHabitacion(
    IN p_numero VARCHAR(50), IN p_piso INT, IN p_tipo VARCHAR(50),
    IN p_orientacion VARCHAR(50), IN p_estado VARCHAR(50), IN p_tarifa DECIMAL(10,2),
    IN p_hotel VARCHAR(50)
)
BEGIN
    UPDATE habitaciones SET piso=p_piso, tipo=p_tipo, orientacion=p_orientacion,
        estado=p_estado, tarifa_base=p_tarifa, hotel_codigo=p_hotel WHERE numero=p_numero;
END$$

DROP PROCEDURE IF EXISTS EliminarHabitacion$$
CREATE PROCEDURE EliminarHabitacion(IN p_numero VARCHAR(50))
BEGIN DELETE FROM habitaciones WHERE numero=p_numero; END$$

DROP PROCEDURE IF EXISTS ActualizarCliente$$
CREATE PROCEDURE ActualizarCliente(
    IN p_id VARCHAR(50), IN p_nombres VARCHAR(100), IN p_apellidos VARCHAR(100),
    IN p_documento VARCHAR(50), IN p_nacionalidad VARCHAR(50), IN p_fecha DATE,
    IN p_direccion VARCHAR(200), IN p_telefono VARCHAR(20), IN p_correo VARCHAR(100),
    IN p_nivel INT
)
BEGIN
    UPDATE clientes SET nombres=p_nombres, apellidos=p_apellidos, documento=p_documento,
        nacionalidad=p_nacionalidad, fecha_nacimiento=p_fecha, direccion=p_direccion,
        telefono=p_telefono, correo=p_correo, nivel_fidelizacion=p_nivel WHERE id=p_id;
END$$

DROP PROCEDURE IF EXISTS EliminarCliente$$
CREATE PROCEDURE EliminarCliente(IN p_id VARCHAR(50))
BEGIN DELETE FROM clientes WHERE id=p_id; END$$

DROP PROCEDURE IF EXISTS ActualizarReserva$$
CREATE PROCEDURE ActualizarReserva(
    IN p_numero VARCHAR(50), IN p_cliente VARCHAR(50), IN p_llegada DATE,
    IN p_salida DATE, IN p_noches INT, IN p_habitaciones INT, IN p_tarifa DECIMAL(10,2)
)
BEGIN
    UPDATE reservas SET cliente_id=p_cliente, fecha_llegada=p_llegada,
        fecha_salida=p_salida, noches=p_noches, habitaciones=p_habitaciones,
        tarifa=p_tarifa WHERE numero=p_numero;
END$$

DROP PROCEDURE IF EXISTS EliminarReserva$$
CREATE PROCEDURE EliminarReserva(IN p_numero VARCHAR(50))
BEGIN DELETE FROM reservas WHERE numero=p_numero; END$$

DROP PROCEDURE IF EXISTS ActualizarTarifa$$
CREATE PROCEDURE ActualizarTarifa(
    IN p_codigo VARCHAR(50), IN p_tipo VARCHAR(50), IN p_temporada VARCHAR(50),
    IN p_base DECIMAL(10,2), IN p_impuestos DECIMAL(10,2),
    IN p_descuento DECIMAL(10,2), IN p_final DECIMAL(10,2)
)
BEGIN
    UPDATE tarifas SET tipo_habitacion=p_tipo, temporada=p_temporada,
        tarifa_base=p_base, impuestos=p_impuestos, descuento=p_descuento,
        precio_final=p_final WHERE codigo=p_codigo;
END$$

DROP PROCEDURE IF EXISTS EliminarTarifa$$
CREATE PROCEDURE EliminarTarifa(IN p_codigo VARCHAR(50))
BEGIN DELETE FROM tarifas WHERE codigo=p_codigo; END$$

DROP PROCEDURE IF EXISTS ActualizarServicio$$
CREATE PROCEDURE ActualizarServicio(
    IN p_codigo VARCHAR(50), IN p_nombre VARCHAR(100), IN p_descripcion VARCHAR(200),
    IN p_horario VARCHAR(50), IN p_precio DECIMAL(10,2)
)
BEGIN
    UPDATE servicios SET nombre=p_nombre, descripcion=p_descripcion,
        horario=p_horario, precio=p_precio WHERE codigo=p_codigo;
END$$

DROP PROCEDURE IF EXISTS EliminarServicio$$
CREATE PROCEDURE EliminarServicio(IN p_codigo VARCHAR(50))
BEGIN DELETE FROM servicios WHERE codigo=p_codigo; END$$

DROP PROCEDURE IF EXISTS ActualizarEvento$$
CREATE PROCEDURE ActualizarEvento(
    IN p_codigo VARCHAR(50), IN p_tipo VARCHAR(50), IN p_cliente VARCHAR(50),
    IN p_fecha DATE, IN p_duracion INT, IN p_asistentes INT,
    IN p_precio DECIMAL(10,2), IN p_estado VARCHAR(50)
)
BEGIN
    UPDATE eventos SET tipo=p_tipo, cliente_id=p_cliente, fecha=p_fecha,
        duracion=p_duracion, asistentes=p_asistentes, precio_total=p_precio,
        estado=p_estado WHERE codigo=p_codigo;
END$$

DROP PROCEDURE IF EXISTS EliminarEvento$$
CREATE PROCEDURE EliminarEvento(IN p_codigo VARCHAR(50))
BEGIN DELETE FROM eventos WHERE codigo=p_codigo; END$$

DROP PROCEDURE IF EXISTS ActualizarSalon$$
CREATE PROCEDURE ActualizarSalon(
    IN p_codigo VARCHAR(50), IN p_nombre VARCHAR(100), IN p_ubicacion VARCHAR(100),
    IN p_capacidad INT, IN p_tamano DECIMAL(10,2), IN p_configuraciones VARCHAR(200),
    IN p_tarifa DECIMAL(10,2)
)
BEGIN
    UPDATE salones SET nombre=p_nombre, ubicacion=p_ubicacion, capacidad=p_capacidad,
        tamano=p_tamano, configuraciones=p_configuraciones, tarifa=p_tarifa
        WHERE codigo=p_codigo;
END$$

DROP PROCEDURE IF EXISTS EliminarSalon$$
CREATE PROCEDURE EliminarSalon(IN p_codigo VARCHAR(50))
BEGIN DELETE FROM salones WHERE codigo=p_codigo; END$$

DROP PROCEDURE IF EXISTS ActualizarConsumo$$
CREATE PROCEDURE ActualizarConsumo(
    IN p_cliente VARCHAR(50), IN p_habitacion VARCHAR(50), IN p_servicio VARCHAR(50),
    IN p_fecha DATE, IN p_cantidad INT, IN p_empleado VARCHAR(100)
)
BEGIN
    UPDATE consumos SET cantidad=p_cantidad,
        total=(SELECT precio FROM servicios WHERE codigo=p_servicio) * p_cantidad,
        empleado=p_empleado
        WHERE cliente_id=p_cliente AND habitacion_numero=p_habitacion
        AND servicio_codigo=p_servicio AND fecha=p_fecha;
END$$

DROP PROCEDURE IF EXISTS EliminarConsumo$$
CREATE PROCEDURE EliminarConsumo(IN p_cliente VARCHAR(50), IN p_habitacion VARCHAR(50), IN p_servicio VARCHAR(50), IN p_fecha DATE)
BEGIN
    DELETE FROM consumos WHERE cliente_id=p_cliente AND habitacion_numero=p_habitacion
        AND servicio_codigo=p_servicio AND fecha=p_fecha;
END$$

DROP PROCEDURE IF EXISTS ActualizarMovimiento$$
CREATE PROCEDURE ActualizarMovimiento(
    IN p_id INT, IN p_reserva VARCHAR(50), IN p_habitacion VARCHAR(50), IN p_tipo VARCHAR(50),
    IN p_empleado VARCHAR(100), IN p_observaciones VARCHAR(255)
)
BEGIN
    UPDATE movimientos SET reserva_numero=p_reserva, habitacion_numero=p_habitacion,
        tipo=p_tipo, empleado=p_empleado, observaciones=p_observaciones WHERE id=p_id;
END$$

DROP PROCEDURE IF EXISTS EliminarMovimiento$$
CREATE PROCEDURE EliminarMovimiento(IN p_id INT)
BEGIN DELETE FROM movimientos WHERE id=p_id; END$$

DELIMITER ;
