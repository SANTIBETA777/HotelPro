from tkinter import ttk

_current_theme = "claro"


def aplicar_estilos(root, theme="claro"):
    global _current_theme
    _current_theme = theme
    style = ttk.Style(root)
    style.theme_use("clam")

    dark = theme == "oscuro"

    if dark:
        background = "#101820"
        panel = "#17242F"
        panel_2 = "#1F2D3A"
        field_background = "#1B2733"
        field_foreground = "#EEF6FF"
        foreground = "#EEF6FF"
        heading_background = "#2A4458"
        title_color = "#82D4FF"
        button_text = "#F8FBFF"
        accent_blue = "#2F80ED"
        accent_blue_dark = "#245DB2"
        accent_green = "#2C8F5D"
        accent_green_dark = "#1F7045"
        accent_red = "#D94D4D"
        accent_red_dark = "#AF3A3A"
        accent_gray = "#4A647A"
        accent_gray_dark = "#2F4859"
    else:
        background = "#f0f0f0"
        panel = "#ffffff"
        panel_2 = "#f8f8f8"
        field_background = "#fafafa"
        field_foreground = "#1f1f1f"
        foreground = "#333333"
        heading_background = "#007ACC"
        title_color = "#004080"
        button_text = "white"
        accent_blue = "#007ACC"
        accent_blue_dark = "#005999"
        accent_green = "#A8E6CF"
        accent_green_dark = "#81C784"
        accent_red = "#FF8A80"
        accent_red_dark = "#E57373"
        accent_gray = "#CFD8DC"
        accent_gray_dark = "#B0BEC5"

    style.configure("Custom.TFrame", background=background)
    style.configure("TFrame", background=background)
    style.configure("TLabel", background=background, foreground=foreground)
    style.configure("TNotebook", background=background)
    style.configure("TEntry",
                    fieldbackground=field_background,
                    foreground=field_foreground,
                    background=field_background)
    style.map("TEntry",
              background=[("active", field_background)],
              foreground=[("disabled", foreground)])
    style.configure("TCombobox",
                    fieldbackground=field_background,
                    background=field_background,
                    foreground=field_foreground)

    style.configure("Titulo.TLabel",
                    font=("Arial", 16, "bold"),
                    foreground=title_color,
                    background=background)

    style.configure("Campo.TLabel",
                    font=("Arial", 11),
                    foreground=foreground,
                    background=background)

    style.configure("Accion.TButton",
                    font=("Arial", 11, "bold"),
                    foreground=button_text,
                    background=accent_blue)
    style.map("Accion.TButton",
              background=[("active", accent_blue_dark)],
              foreground=[("active", button_text)])

    style.configure("Registrar.TButton",
                    font=("Arial", 11, "bold"),
                    foreground=("black" if not dark else "white"),
                    background=accent_green)
    style.map("Registrar.TButton",
              background=[("active", accent_green_dark)],
              foreground=[("active", "black" if not dark else "white")])

    style.configure("Editar.TButton",
                    font=("Arial", 11, "bold"),
                    foreground=("black" if not dark else "white"),
                    background=("#81D4FA" if not dark else accent_blue))
    style.map("Editar.TButton",
              background=[("active", ("#4FC3F7" if not dark else accent_blue_dark))],
              foreground=[("active", "black" if not dark else "white")])

    style.configure("Buscar.TButton",
                    font=("Arial", 11, "bold"),
                    foreground=("black" if not dark else "white"),
                    background=("#CFD8DC" if not dark else accent_gray))
    style.map("Buscar.TButton",
              background=[("active", ("#B0BEC5" if not dark else accent_gray_dark))],
              foreground=[("active", "black" if not dark else "white")])

    style.configure("Eliminar.TButton",
                    font=("Arial", 11, "bold"),
                    foreground=("black" if not dark else "white"),
                    background=("#FF8A80" if not dark else accent_red))
    style.map("Eliminar.TButton",
              background=[("active", ("#E57373" if not dark else accent_red_dark))],
              foreground=[("active", "black" if not dark else "white")])

    style.configure("TNotebook.Tab",
                    padding=[10, 5],
                    font=("Arial", 11, "bold"),
                    background=("#DADADA" if not dark else panel_2),
                    foreground=foreground)
    style.map("TNotebook.Tab",
              background=[("selected", ("#F5F5F5" if not dark else panel)), ("active", ("#E6E6E6" if not dark else panel_2))],
              foreground=[("selected", ("#1F1F1F" if not dark else "#EAF2FF")), ("active", foreground)])
    if dark:
        style.configure("TNotebook",
                        background=background,
                        borderwidth=0)
        style.configure("TNotebook.Tab",
                        borderwidth=0,
                        relief="flat")
        style.map("TNotebook.Tab",
                  background=[("selected", panel), ("active", panel_2)],
                  foreground=[("selected", "#EAF2FF"), ("active", "#D7E7FF")])

    style.configure("Treeview",
                    font=("Arial", 10),
                    rowheight=25,
                    background=field_background,
                    fieldbackground=field_background,
                    foreground=field_foreground)
    style.configure("Treeview.Heading",
                    font=("Arial", 10, "bold"),
                    background=heading_background,
                    foreground=button_text)
    style.map("Treeview",
              background=[("selected", accent_blue)],
              foreground=[("selected", "white")])
    style.configure("Preview.TLabel",
                    font=("Arial", 11, "bold"),
                    foreground=foreground,
                    background=field_background,
                    anchor="center")
    style.configure("Preview.TFrame", background=field_background)

    style.configure("Horizontal.TScrollbar", background=panel_2, troughcolor=background)
    style.configure("Vertical.TScrollbar", background=panel_2, troughcolor=background)


def alternar_tema(root):
    aplicar_estilos(root, "oscuro" if _current_theme == "claro" else "claro")
