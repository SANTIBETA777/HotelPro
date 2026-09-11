from tkinter import ttk

def aplicar_estilos(root):
    style = ttk.Style(root)
    style.theme_use("clam")  # Tema base, puedes cambiar a "arc" o "equilux"

    # Fondo general
    style.configure("Custom.TFrame", background="#f0f0f0")

    # Estilo para títulos (ej: "Gestión de Hoteles")
    style.configure("Titulo.TLabel",
                    font=("Arial", 16, "bold"),
                    foreground="#004080",
                    background="#f0f0f0")

    # Estilo para labels de campos (ej: "Reserva Nº")
    style.configure("Campo.TLabel",
                    font=("Arial", 11),
                    foreground="#333333",
                    background="#f0f0f0")

    # Estilo para botones genéricos con hover
    style.configure("Accion.TButton",
                    font=("Arial", 11, "bold"),
                    foreground="white",
                    background="#007ACC")
    style.map("Accion.TButton",
                background=[("active", "#005999")],
                foreground=[("active", "white")])

    # 🔽 Botones específicos con colores pastel
    style.configure("Registrar.TButton",
                    font=("Arial", 11, "bold"),
                    foreground="black",
                    background="#A8E6CF")  # Verde pastel
    style.map("Registrar.TButton",
                background=[("active", "#81C784")],
                foreground=[("active", "black")])

    style.configure("Editar.TButton",
                    font=("Arial", 11, "bold"),
                    foreground="black",
                    background="#81D4FA")  # Azul pastel
    style.map("Editar.TButton",
                background=[("active", "#4FC3F7")],
                foreground=[("active", "black")])

    style.configure("Buscar.TButton",
                    font=("Arial", 11, "bold"),
                    foreground="black",
                    background="#CFD8DC")  # Gris claro pastel
    style.map("Buscar.TButton",
                background=[("active", "#B0BEC5")],
                foreground=[("active", "black")])

    style.configure("Eliminar.TButton",
                    font=("Arial", 11, "bold"),
                    foreground="black",
                    background="#FF8A80")  # Rojo coral pastel
    style.map("Eliminar.TButton",
                background=[("active", "#E57373")],
                foreground=[("active", "black")])

    # Estilo para pestañas del Notebook
    style.configure("TNotebook.Tab",
                    padding=[10, 5],
                    font=("Arial", 11, "bold"))

    # Estilo para tablas (Treeview)
    style.configure("Treeview",
                    font=("Arial", 10),
                    rowheight=25,
                    background="#fafafa",
                    fieldbackground="#fafafa")
    style.configure("Treeview.Heading",
                    font=("Arial", 10, "bold"),
                    background="#007ACC",
                    foreground="white")
