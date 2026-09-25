📄 README.md

# HotelPro 🏨
Sistema de gestión hotelera desarrollado en **Python + Tkinter** con conexión a **MySQL**.  
Incluye módulos para clientes, reservas, habitaciones, hoteles, servicios, salones, eventos y consumos, con interfaz gráfica amigable y una estructura modular para facilitar su mantenimiento y extensión.

---

## 🎯 Objetivo del proyecto
HotelPro tiene como finalidad digitalizar la administración de un hotel, permitiendo gestionar de forma centralizada los procesos principales del negocio, tales como:

- registro y actualización de clientes
- administración de hoteles y habitaciones
- control de reservas
- gestión de tarifas y servicios
- manejo de eventos y salones
- registro de consumos
- control de check-in y check-out

El sistema busca mejorar la organización operativa, reducir errores manuales y facilitar la toma de decisiones mediante una interfaz gráfica intuitiva.

---

## 🚀 Instalación

### 1. Clonar o descargar el proyecto
Ubica la carpeta `HotelPro` en tu entorno de trabajo.

### 2. Crear entorno virtual

```bash
python -m venv venv
```

Activar entorno:

Windows (PowerShell):

```powershell
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 3. Instalar dependencias
El proyecto usa un archivo `requirements.txt` con las librerías necesarias:

```bash
pip install -r requirements.txt
```

Dependencias actuales:

```text
mysql-connector-python
Pillow
openpyxl
reportlab
tkcalendar
```

> Tkinter ya viene incluido en Python, por lo que no es necesario agregarlo manualmente.

### 4. Configurar base de datos
Antes de ejecutar la aplicación, debes tener MySQL corriendo en tu sistema (XAMPP, WampServer u otra instalación local).

1. Crear la base de datos `hotelpro`.
2. Importar el script SQL de creación de tablas y relaciones.
3. Ejecutar el archivo `procedimientos_crud.sql` para dejar disponibles los procedimientos de actualización y eliminación empleados por la aplicación.

> El proyecto está pensado para trabajar con MySQL. Es importante mantener la base de datos creada y configurada correctamente antes de abrir la interfaz.

---

## ▶️ Ejecución
Dentro de la carpeta raíz del proyecto:

```bash
python main.py
```

Esto abrirá la interfaz gráfica de HotelPro con pestañas para gestionar:

- Clientes
- Hoteles
- Habitaciones
- Reservas
- Check-In / Check-Out
- Tarifas
- Servicios
- Consumos
- Eventos
- Salones

Cada módulo incluye botones para exportar el contenido del Treeview a Excel (`.xlsx`) o PDF (`.pdf`). Antes de exportar, se puede aplicar un criterio de búsqueda y un rango de fechas.

---

## 🗄️ Base de datos
La aplicación utiliza MySQL como motor principal para almacenar la información del sistema. La lógica de conexión se encuentra en `database.py`, y todas las operaciones de alta, baja, modificación y consulta se realizan a través de procedimientos almacenados y consultas SQL.

Para el correcto funcionamiento del sistema, es necesario contar con la base de datos `hotelpro` creada en MySQL, junto con las tablas principales y los procedimientos almacenados definidos en `procedimientos_crud.sql`.

Entre los elementos principales de la base de datos están:

- clientes
- hoteles
- habitaciones
- reservas
- tarifas
- servicios
- consumos
- eventos
- salones
- movimientos/check-in y check-out

La relación entre tablas permite controlar datos del hotel, de clientes, de habitaciones y de operaciones del negocio de manera organizada.

---

## 📂 Estructura del proyecto

```text
HotelPro/
├─ main.py                 # Punto de entrada principal
├─ database.py             # Conexión y funciones CRUD con MySQL
├─ requirements.txt        # Dependencias del proyecto
├─ procedimientos_crud.sql # Procedimientos de actualización y eliminación
├─ README.md               # Documentación del proyecto
├─ hotelpro.db             # Base de datos local de respaldo
├─ modulos/                # Lógica del negocio (POO)
│  ├─ cliente.py
│  ├─ consumo.py
│  ├─ evento.py
│  ├─ habitacion.py
│  ├─ hotel.py
│  ├─ reserva.py
│  ├─ salon.py
│  ├─ servicio.py
│  └─ tarifa.py
├─ ui/                     # Interfaces gráficas Tkinter
│  ├─ checkin_checkout_ui.py
│  ├─ clientes_ui.py
│  ├─ consumo_ui.py
│  ├─ eventos_ui.py
│  ├─ export_utils.py
│  ├─ form_utils.py
│  ├─ habitaciones_ui.py
│  ├─ hoteles_ui.py
│  ├─ main.py
│  ├─ reservas_ui.py
│  ├─ salon_ui.py
│  ├─ servicios_ui.py
│  ├─ style.py
│  ├─ tarifas_ui.py
│  ├─ tooltip.py
└─
```

> En algunos entornos puede ser necesario verificar la ruta y el nombre exacto de los archivos dentro de la carpeta `ui` antes de ejecutar la aplicación.

---

## 🧪 Pruebas funcionales sugeridas
Para comprobar que el sistema funciona correctamente, se recomienda ejecutar estas pruebas básicas:

1. Registrar un hotel.
2. Crear una o varias habitaciones.
3. Agregar un cliente.
4. Crear una reserva con fecha de entrada y salida.
5. Realizar check-in.
6. Agregar consumo de servicio.
7. Realizar check-out.
8. Editar y eliminar registros desde cada módulo.
9. Exportar información a Excel y PDF.

Estas pruebas permiten validar que la interfaz, los formularios y la conexión con la base de datos funcionan correctamente.

---

## ✅ Criterios de entrega esperados
Para una entrega final de proyecto, normalmente se solicita que el sistema incluya:

- interfaz gráfica funcional
- módulos principales completos
- conexión con base de datos
- uso de procedimientos o consultas SQL
- manejo de errores
- validación de datos
- documentación de funcionamiento
- prueba del sistema en ejecución

Este proyecto cumple con ese enfoque, y el README sirve como guía para comprender la instalación, la estructura y la operación del sistema.

---

## 🛠️ Tecnologías usadas

- Python 3.10+
- Tkinter / ttk
- MySQL Connector
- MySQL / XAMPP / WampServer / HeidiSQL
- SQLite (si se usa como respaldo local en pruebas puntuales)

---

## 📌 Notas importantes
- Asegúrate de tener MySQL corriendo antes de abrir la aplicación.
- Verifica que la base de datos `hotelpro` exista y que los procedimientos SQL estén importados correctamente.
- Si agregas nuevas librerías externas, recuerda añadirlas al archivo `requirements.txt`.
- Mantén la estructura de módulos ordenada para facilitar el mantenimiento futuro.

---

## 🔗 Enlaces relevantes

GitHub:  
https://github.com/SANTIBETA777/HotelPro/blob/main/main.py

Video explicativo de la interfaz y funcionamiento:  
https://share.vidyard.com/watch/D8a6DkLdf2mk6EuFbqs56o

Presentación Genially:  
https://view.genially.com/6aa59eaec719f710592c17a3

---

## 📎 Estado del proyecto
HotelPro se encuentra en una etapa funcional con una interfaz gráfica y módulos principales desarrollados. La parte clave para dejar la entrega más sólida es validar la base de datos en MySQL, realizar pruebas reales del flujo de negocio y documentar claramente la operación del sistema para la evaluación final.

---

## 📝 Resumen ejecutivo
HotelPro es un proyecto de gestión hotelera desarrollado en Python con interfaz gráfica en Tkinter, orientado a la administración de operaciones diarias de un establecimiento. El sistema abarca desde la gestión de clientes y habitaciones hasta reservas, consumos y eventos, con el objetivo de ofrecer una solución práctica y organizada para la administración del negocio.

La aplicación está diseñada para ser extensible y fácil de mantener, reutilizando una estructura modular en la carpeta `modulos` y una capa visual separada en la carpeta `ui`, lo que facilita la evolución del sistema a futuro.

Este README sirve como guía principal para instalación, ejecución, configuración de la base de datos y presentación del proyecto ante el profesor o la evaluación final.