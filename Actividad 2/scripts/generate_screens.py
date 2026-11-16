#!/usr/bin/env python3
"""Genera mockups PNG de pantallas SeguritoApp (iPhone 390x844) para Figma/PDF."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "assets" / "screens"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 390, 844
BARK = (27, 58, 47)
LEAF = (47, 107, 79)
LEAF_SOFT = (231, 242, 236)
CANOPY = (15, 36, 28)
CLOUD = (244, 247, 245)
PAPER = (255, 255, 255)
MUTED = (93, 114, 104)
LINE = (215, 227, 220)
SUN = (212, 160, 23)
OK = (6, 118, 71)
WARN = (181, 71, 8)
DANGER = (180, 35, 24)


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size, index=0)
        except Exception:
            continue
    return ImageFont.load_default()


def rounded(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def status(draw, dark=False):
    color = (255, 255, 255) if dark else CANOPY
    draw.text((22, 16), "9:41", font=font(12, True), fill=color)
    draw.text((300, 16), "LTE 80%", font=font(11), fill=color)


def topbar(draw, title, back=False):
    if back:
        rounded(draw, (18, 48, 54, 84), 12, PAPER, LINE)
        draw.text((28, 56), "←", font=font(16), fill=BARK)
    draw.text((120 if back else 24, 56), title, font=font(20, True), fill=CANOPY)


def nav(draw, active=0):
    rounded(draw, (12, 760, 378, 828), 22, PAPER, LINE)
    labels = ["Inicio", "Afiliados", "Solicitudes", "Avisos"]
    icons = ["⌂", "+", "=", "*"]
    xs = [40, 125, 215, 305]
    for i, (x, lab, ic) in enumerate(zip(xs, labels, icons)):
        color = LEAF if i == active else MUTED
        draw.text((x + 8, 772), ic, font=font(14), fill=color)
        draw.text((x, 796), lab, font=font(10), fill=color)


def save(img, name):
    path = OUT / f"{name}.png"
    img.save(path, "PNG")
    print(path)


def screen_login():
    img = Image.new("RGB", (W, H), CANOPY)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(33 + (15 - 33) * t)
        g = int(76 + (36 - 76) * t)
        b = int(58 + (28 - 58) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    status(draw, dark=True)
    rounded(draw, (22, 70, 86, 134), 20, LEAF)
    # Árbol simple (marca El Gran Árbol)
    draw.polygon([(54, 82), (38, 108), (70, 108)], fill=PAPER)
    draw.rectangle((51, 108, 57, 122), fill=(232, 214, 160))
    draw.text((22, 150), "SeguritoApp", font=font(34, True), fill=PAPER)
    draw.text((22, 198), "Tu red afiliada y autorizaciones", font=font(14), fill=(220, 235, 228))
    draw.text((22, 218), "médicas con El Gran Árbol.", font=font(14), fill=(220, 235, 228))
    rounded(draw, (18, 430, 372, 800), 24, PAPER)
    draw.text((38, 455), "Iniciar sesión", font=font(20, True), fill=CANOPY)
    draw.text((38, 485), "Ingresa tus credenciales para continuar", font=font(12), fill=MUTED)
    draw.text((38, 525), "Correo", font=font(12, True), fill=BARK)
    rounded(draw, (38, 545, 352, 585), 14, CLOUD, LINE)
    draw.text((38, 605), "Contraseña", font=font(12, True), fill=BARK)
    rounded(draw, (38, 625, 352, 665), 14, CLOUD, LINE)
    rounded(draw, (38, 700, 352, 748), 14, LEAF)
    draw.text((150, 714), "Ingresar", font=font(15, True), fill=PAPER)
    save(img, "01_login")


def screen_home():
    img = Image.new("RGB", (W, H), CLOUD)
    draw = ImageDraw.Draw(img)
    status(draw)
    topbar(draw, "SeguritoApp")
    rounded(draw, (18, 100, 372, 220), 22, BARK)
    draw.ellipse((280, 70, 420, 210), fill=(212, 160, 23, 40) if False else (60, 100, 70))
    draw.text((34, 118), "Hola, Otto", font=font(12), fill=(210, 225, 218))
    draw.text((34, 140), "El Gran Árbol", font=font(22, True), fill=PAPER)
    draw.text((34, 168), "cuida tu salud", font=font(22, True), fill=PAPER)
    rounded(draw, (34, 200, 230, 222), 12, (40, 80, 60))
    draw.text((44, 204), "Póliza GA-08001620", font=font(10), fill=PAPER)

    tiles = [
        (18, 240, "Médicos", "Red afiliada"),
        (200, 240, "Hospitales", "Centros"),
        (18, 370, "Laboratorios", "Estudios"),
        (200, 370, "Nueva sol.", "Autorizar"),
    ]
    for x, y, t, s in tiles:
        rounded(draw, (x, y, x + 172, y + 118), 18, PAPER, LINE)
        rounded(draw, (x + 14, y + 14, x + 54, y + 54), 14, LEAF_SOFT)
        draw.text((x + 14, y + 70), t, font=font(14, True), fill=CANOPY)
        draw.text((x + 14, y + 92), s, font=font(11), fill=MUTED)

    draw.text((18, 510), "RESUMEN", font=font(11, True), fill=BARK)
    rounded(draw, (18, 535, 186, 610), 16, PAPER, LINE)
    rounded(draw, (202, 535, 372, 610), 16, PAPER, LINE)
    draw.text((34, 550), "1", font=font(24, True), fill=CANOPY)
    draw.text((34, 582), "En revisión", font=font(11), fill=MUTED)
    draw.text((218, 550), "2", font=font(24, True), fill=CANOPY)
    draw.text((218, 582), "Avisos nuevos", font=font(11), fill=MUTED)
    nav(draw, 0)
    save(img, "02_home")


def screen_afiliados():
    img = Image.new("RGB", (W, H), CLOUD)
    draw = ImageDraw.Draw(img)
    status(draw)
    topbar(draw, "Afiliados")
    chips = [("Médicos", True), ("Hospitales", False), ("Labs", False)]
    x = 18
    for label, active in chips:
        w = 92 if label != "Hospitales" else 110
        rounded(draw, (x, 100, x + w, 134), 16, LEAF if active else PAPER, None if active else LINE)
        draw.text((x + 14, 110), label, font=font(12, True), fill=PAPER if active else MUTED)
        x += w + 8
    rounded(draw, (18, 150, 372, 190), 14, PAPER, LINE)
    draw.text((32, 162), "Buscar por nombre, especialidad o zona", font=font(11), fill=MUTED)

    docs = [
        ("AL", "Dra. Ana Lucía Méndez", "Medicina interna · Zona 10"),
        ("CR", "Dr. Carlos Rivera", "Cardiología · Zona 15"),
        ("SC", "Dra. Sofía Castillo", "Pediatría · Zona 9"),
        ("LP", "Dr. Luis Paredes", "Traumatología · Zona 11"),
    ]
    y = 210
    for initials, name, meta in docs:
        rounded(draw, (18, y, 372, y + 78), 18, PAPER, LINE)
        rounded(draw, (30, y + 15, 78, y + 63), 16, LEAF_SOFT)
        draw.text((42, y + 28), initials, font=font(13, True), fill=LEAF)
        draw.text((92, y + 20), name, font=font(13, True), fill=CANOPY)
        draw.text((92, y + 44), meta, font=font(11), fill=MUTED)
        y += 90
    nav(draw, 1)
    save(img, "03_afiliados_medicos")


def screen_detalle():
    img = Image.new("RGB", (W, H), CLOUD)
    draw = ImageDraw.Draw(img)
    status(draw)
    topbar(draw, "Detalle", back=True)
    rounded(draw, (18, 100, 372, 430), 18, PAPER, LINE)
    rounded(draw, (34, 120, 98, 184), 20, LEAF_SOFT)
    draw.text((50, 140), "AL", font=font(18, True), fill=LEAF)
    draw.text((34, 200), "Dra. Ana Lucía Méndez", font=font(18, True), fill=CANOPY)
    draw.text((34, 228), "Medicina interna", font=font(13), fill=MUTED)
    rows = [("Zona", "Zona 10"), ("Teléfono", "2222-1101"), ("Horario", "Lun–Vie 8:00–16:00"), ("Estado", "Afiliado activo")]
    y = 265
    for k, v in rows:
        draw.text((34, y), k, font=font(12), fill=MUTED)
        draw.text((220, y), v, font=font(12, True), fill=BARK)
        draw.line((34, y + 22, 356, y + 22), fill=LINE)
        y += 34
    rounded(draw, (18, 450, 372, 498), 14, LEAF)
    draw.text((100, 464), "Solicitar autorización", font=font(14, True), fill=PAPER)
    nav(draw, 1)
    save(img, "04_detalle_afiliado")


def screen_nueva():
    img = Image.new("RGB", (W, H), CLOUD)
    draw = ImageDraw.Draw(img)
    status(draw)
    topbar(draw, "Nueva solicitud", back=True)
    rounded(draw, (18, 100, 372, 148), 14, PAPER, LINE)
    rounded(draw, (24, 106, 190, 142), 10, LEAF_SOFT)
    draw.text((55, 116), "Medicamento", font=font(12, True), fill=LEAF)
    draw.text((230, 116), "Hospitalización", font=font(12, True), fill=MUTED)
    rounded(draw, (18, 168, 372, 560), 18, PAPER, LINE)
    draw.text((34, 188), "Autorización de medicamento", font=font(16, True), fill=CANOPY)
    draw.text((34, 215), "Completa los datos. Quedará registrada", font=font(11), fill=MUTED)
    draw.text((34, 232), "y recibirás notificación de respuesta.", font=font(11), fill=MUTED)
    for label, y in [("Medicamento", 270), ("Detalle", 350), ("Médico tratante", 430)]:
        draw.text((34, y), label, font=font(12, True), fill=BARK)
        rounded(draw, (34, y + 22, 356, y + 60), 12, CLOUD, LINE)
    rounded(draw, (34, 510, 356, 548), 12, LEAF)
    draw.text((130, 522), "Enviar solicitud", font=font(13, True), fill=PAPER)
    nav(draw, 2)
    save(img, "05_nueva_medicamento")


def screen_solicitudes():
    img = Image.new("RGB", (W, H), CLOUD)
    draw = ImageDraw.Draw(img)
    status(draw)
    topbar(draw, "Solicitudes")
    chips = [("Todas", True), ("Revisión", False), ("Aprobadas", False), ("Rechazadas", False)]
    x = 18
    for label, active in chips:
        w = 70 if label == "Todas" else (78 if label == "Revisión" else 92)
        rounded(draw, (x, 100, x + w, 132), 14, LEAF if active else PAPER, None if active else LINE)
        draw.text((x + 10, 109), label, font=font(10, True), fill=PAPER if active else MUTED)
        x += w + 6

    items = [
        ("SOL-1001", "Losartán 50 mg", "Aprobada", OK, (236, 253, 243)),
        ("SOL-1002", "Hospitalización programada", "En revisión", WARN, (255, 250, 235)),
        ("SOL-1003", "Amoxicilina 500 mg", "Rechazada", DANGER, (254, 243, 242)),
    ]
    y = 150
    for sid, title, st, color, bg in items:
        rounded(draw, (18, y, 372, y + 88), 18, PAPER, LINE)
        draw.text((34, y + 18), title, font=font(14, True), fill=CANOPY)
        draw.text((34, y + 42), f"{sid} · registro de autorización", font=font(11), fill=MUTED)
        rounded(draw, (250, y + 16, 356, y + 40), 10, bg)
        draw.text((262, y + 20), st, font=font(10, True), fill=color)
        y += 100
    nav(draw, 2)
    save(img, "06_solicitudes")


def screen_detalle_sol():
    img = Image.new("RGB", (W, H), CLOUD)
    draw = ImageDraw.Draw(img)
    status(draw)
    topbar(draw, "Detalle", back=True)
    rounded(draw, (18, 100, 372, 420), 18, PAPER, LINE)
    draw.text((34, 120), "Losartán 50 mg", font=font(18, True), fill=CANOPY)
    rounded(draw, (260, 120, 350, 144), 10, (236, 253, 243))
    draw.text((274, 124), "Aprobada", font=font(10, True), fill=OK)
    draw.text((34, 155), "Medicamento · SOL-1001", font=font(12), fill=MUTED)
    rows = [("Fecha", "2026-11-05"), ("Médico", "Dra. Ana Lucía Méndez"), ("Detalle", "30 tabletas")]
    y = 195
    for k, v in rows:
        draw.text((34, y), k, font=font(12), fill=MUTED)
        draw.text((180, y), v, font=font(12, True), fill=BARK)
        y += 30
    draw.text((34, 300), "SEGUIMIENTO", font=font(11, True), fill=BARK)
    draw.line((42, 330, 42, 390), fill=LINE, width=2)
    draw.ellipse((36, 328, 48, 340), fill=LEAF)
    draw.text((60, 326), "Solicitud enviada", font=font(12, True), fill=CANOPY)
    draw.text((60, 344), "2026-11-05", font=font(11), fill=MUTED)
    draw.ellipse((36, 370, 48, 382), fill=LEAF)
    draw.text((60, 368), "Aprobada", font=font(12, True), fill=CANOPY)
    draw.text((60, 386), "Autorizado por 30 días.", font=font(11), fill=MUTED)
    nav(draw, 2)
    save(img, "07_detalle_solicitud")


def screen_notificaciones():
    img = Image.new("RGB", (W, H), CLOUD)
    draw = ImageDraw.Draw(img)
    status(draw)
    topbar(draw, "Notificaciones")
    notes = [
        ("✓", "Autorización aprobada", "SOL-1001 · Losartán 50 mg", (236, 253, 243), True),
        ("…", "Autorización en revisión", "SOL-1002 · Hospitalización", (255, 250, 235), True),
        ("!", "Autorización rechazada", "SOL-1003 · Amoxicilina", (254, 243, 242), False),
    ]
    y = 100
    for icon, title, body, bg, unread in notes:
        rounded(draw, (18, y, 372, y + 86), 18, PAPER, LINE)
        if unread:
            draw.rectangle((18, y + 10, 21, y + 76), fill=SUN)
        rounded(draw, (34, y + 18, 76, y + 60), 14, bg)
        draw.text((48, y + 28), icon, font=font(14, True), fill=BARK)
        draw.text((90, y + 20), title, font=font(13, True), fill=CANOPY)
        draw.text((90, y + 44), body, font=font(11), fill=MUTED)
        y += 100
    nav(draw, 3)
    save(img, "08_notificaciones")


def screen_hospitalizacion():
    img = Image.new("RGB", (W, H), CLOUD)
    draw = ImageDraw.Draw(img)
    status(draw)
    topbar(draw, "Nueva solicitud", back=True)
    rounded(draw, (18, 100, 372, 148), 14, PAPER, LINE)
    draw.text((55, 116), "Medicamento", font=font(12, True), fill=MUTED)
    rounded(draw, (200, 106, 366, 142), 10, LEAF_SOFT)
    draw.text((220, 116), "Hospitalización", font=font(12, True), fill=LEAF)
    rounded(draw, (18, 168, 372, 500), 18, PAPER, LINE)
    draw.text((34, 188), "Autorización de hospitalización", font=font(15, True), fill=CANOPY)
    for label, y in [("Motivo / procedimiento", 240), ("Detalle", 320), ("Médico tratante", 400)]:
        draw.text((34, y), label, font=font(12, True), fill=BARK)
        rounded(draw, (34, y + 22, 356, y + 60), 12, CLOUD, LINE)
    rounded(draw, (34, 470, 356, 508) if False else (34, 448, 356, 486), 12, LEAF)
    draw.text((130, 460), "Enviar solicitud", font=font(13, True), fill=PAPER)
    nav(draw, 2)
    save(img, "09_nueva_hospitalizacion")


def screen_flow():
    """Mapa de flujo para importar como frame de overview en Figma."""
    img = Image.new("RGB", (1400, 900), (238, 245, 241))
    draw = ImageDraw.Draw(img)
    draw.text((48, 36), "SeguritoApp · Flujo de prototipo", font=font(28, True), fill=CANOPY)
    draw.text((48, 78), "El Gran Árbol · Otto Hernandez · 08001620", font=font(14), fill=MUTED)
    boxes = [
        (60, 160, "Login"),
        (280, 160, "Inicio"),
        (500, 80, "Afiliados"),
        (500, 160, "Detalle"),
        (500, 240, "Nueva sol."),
        (760, 120, "Solicitudes"),
        (760, 220, "Detalle sol."),
        (1020, 160, "Notificaciones"),
    ]
    for x, y, label in boxes:
        rounded(draw, (x, y, x + 160, y + 56), 14, PAPER, LEAF, 2)
        draw.text((x + 20, y + 18), label, font=font(14, True), fill=CANOPY)
    # arrows as lines
    lines = [
        (220, 188, 280, 188),
        (440, 188, 500, 188),
        (660, 188, 760, 148),
        (660, 188, 760, 248),
        (920, 188, 1020, 188),
        (440, 108, 500, 108),
        (580, 136, 580, 160),
        (580, 216, 580, 240),
    ]
    for x1, y1, x2, y2 in lines:
        draw.line((x1, y1, x2, y2), fill=LEAF, width=3)
    save(img, "00_flujo")


if __name__ == "__main__":
    screen_flow()
    screen_login()
    screen_home()
    screen_afiliados()
    screen_detalle()
    screen_nueva()
    screen_hospitalizacion()
    screen_solicitudes()
    screen_detalle_sol()
    screen_notificaciones()
    print(f"Generated screens in {OUT}")
