import re
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageTk


EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
NUMBER_PATTERN = re.compile(r"^\d+(\.\d+)?$")
TEXT_PATTERN = re.compile(r"^[\w\s.,:/()%+\-]+$", re.UNICODE)
SUPPORTED_IMAGE_FORMATS = {"JPEG", "PNG", "GIF"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024


def ensure_hotelpro_icon():
    base_dir = Path(__file__).resolve().parent.parent
    assets_dir = base_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    icon_png = assets_dir / "hotelpro_icon.png"
    icon_ico = assets_dir / "hotelpro_icon.ico"

    if not icon_png.exists() or not icon_ico.exists():
        size = 256
        image = Image.new("RGBA", (size, size), (15, 23, 42, 255))
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle((18, 18, 238, 238), radius=36, fill=(20, 35, 64, 255), outline=(78, 121, 255, 255), width=8)

        roof = [(58, 92), (128, 40), (198, 92)]
        draw.polygon(roof, fill=(246, 190, 70, 255))

        draw.rounded_rectangle((78, 96, 178, 182), radius=18, fill=(50, 98, 214, 255))

        for x in (94, 126, 158):
            draw.rectangle((x, 116, x + 18, 142), fill=(226, 238, 255, 255))

        draw.rectangle((94, 148, 162, 180), fill=(255, 255, 255, 255))
        draw.rounded_rectangle((92, 188, 164, 224), radius=14, fill=(246, 190, 70, 255))
        draw.text((128, 206), "H", fill=(15, 23, 42, 255), anchor="mm")

        image.save(icon_png, format="PNG")

        sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        icons = []
        for s in sizes:
            resized = image.resize(s, Image.LANCZOS)
            icons.append(resized)

        icons[0].save(icon_ico, format="ICO", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

    return str(icon_png), str(icon_ico)


def validate_numeric(parent, fields, integer_fields=(), required=True):
    for label, entry in fields:
        value = entry.get().strip()
        if not value and not required:
            continue
        if not value or not NUMBER_PATTERN.fullmatch(value):
            messagebox.showerror("Dato invalido", f"{label}: escribe un numero valido.", parent=parent)
            entry.focus_set()
            return False
        if label in integer_fields and not value.isdigit():
            messagebox.showerror("Dato invalido", f"{label}: debe ser un numero entero.", parent=parent)
            entry.focus_set()
            return False
    return True


def validate_text(parent, fields, minimum=2, maximum=100, required=True):
    for label, entry in fields:
        value = entry.get().strip()
        if not value and not required:
            continue
        if not minimum <= len(value) <= maximum:
            messagebox.showerror(
                "Texto invalido",
                f"{label}: debe tener entre {minimum} y {maximum} caracteres.",
                parent=parent,
            )
            entry.focus_set()
            return False
        if not TEXT_PATTERN.fullmatch(value):
            messagebox.showerror(
                "Texto invalido",
                f"{label}: contiene caracteres especiales no permitidos.",
                parent=parent,
            )
            entry.focus_set()
            return False
    return True


def validate_email(parent, label, entry):
    value = entry.get().strip()
    if not EMAIL_PATTERN.fullmatch(value):
        messagebox.showerror("Correo invalido", f"{label}: escribe un correo valido.", parent=parent)
        entry.focus_set()
        return False
    return True


def confirm_action(parent, title, message):
    return messagebox.askyesno(title, message, parent=parent)


def select_image(parent, entry, preview_label=None, preview_size=(180, 100)):
    path = filedialog.askopenfilename(
        parent=parent,
        title="Seleccionar imagen",
        filetypes=[("Imagenes", "*.jpg *.jpeg *.png *.gif")],
    )
    if not path:
        return False
    try:
        image_path = Path(path)
        if image_path.stat().st_size > MAX_IMAGE_BYTES:
            messagebox.showerror("Imagen invalida", "La imagen no puede superar 5 MB.", parent=parent)
            return False
        with Image.open(path) as image:
            if image.format not in SUPPORTED_IMAGE_FORMATS:
                messagebox.showerror("Imagen invalida", "Solo se permiten JPG, PNG o GIF.", parent=parent)
                return False
            image.verify()
        with Image.open(path) as image:
            image = ImageOps.autocontrast(image.convert("RGB"))
            image = image.filter(ImageFilter.SHARPEN)
            image.thumbnail(preview_size)
            if preview_label is not None:
                preview = ImageTk.PhotoImage(image)
                preview_label.configure(image=preview, text="")
                preview_label.image = preview
        entry.delete(0, "end")
        entry.insert(0, str(image_path))
        return True
    except (OSError, ValueError) as error:
        messagebox.showerror("Imagen invalida", f"No se pudo abrir la imagen: {error}", parent=parent)
        return False


def add_image_field(parent, row, label, entry, preview_label=None, preview_size=(180, 100), include_button=True):
    ttk.Label(parent, text=label, style="Campo.TLabel").grid(row=row, column=0, sticky="w", pady=3)
    entry.grid(row=row, column=1, pady=3)
    if include_button:
        ttk.Button(
            parent,
            text="Seleccionar imagen",
            command=lambda: select_image(parent.winfo_toplevel(), entry, preview_label, preview_size),
            style="Accion.TButton",
        ).grid(row=row, column=2, padx=5, pady=3)
    if preview_label is not None:
        preview_label.grid(row=row, column=3, padx=5, pady=3)


def set_form_icon(window, color=None):
    try:
        icon_png, icon_ico = ensure_hotelpro_icon()
        icon = ImageTk.PhotoImage(Image.open(icon_png))
        window.iconphoto(True, icon)

        try:
            window.iconbitmap(default=icon_ico)
            window.wm_iconbitmap(icon_ico)
        except Exception:
            try:
                window.iconbitmap(default=icon_png)
            except Exception:
                pass

        icons = getattr(window, "_hotelpro_icons", [])
        icons.append(icon)
        window._hotelpro_icons = icons
        return
    except Exception:
        pass

    image = Image.new("RGBA", (32, 32), color or "#007ACC")
    icon = ImageTk.PhotoImage(image)
    window.iconphoto(True, icon)
    icons = getattr(window, "_hotelpro_icons", [])
    icons.append(icon)
    window._hotelpro_icons = icons
