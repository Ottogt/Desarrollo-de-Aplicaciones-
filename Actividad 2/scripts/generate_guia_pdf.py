#!/usr/bin/env python3
"""Guía de usabilidad SeguritoApp en PDF con carátula."""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "Guia_Usabilidad_SeguritoApp_OttoHernandez_08001620.pdf"
SCREENS = ROOT / "assets" / "screens"
OUT.parent.mkdir(parents=True, exist_ok=True)

FONT = "Helvetica"
FONT_B = "Helvetica-Bold"
try:
    pdfmetrics.registerFont(TTFont("Body", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"))
    FONT = "Body"
    FONT_B = "Body"
except Exception:
    pass

W, H = letter
MARGIN = 0.85 * inch

# Colores
BARK = (0.106, 0.227, 0.184)
LEAF = (0.184, 0.420, 0.310)
MUTED = (0.35, 0.42, 0.39)
SUN = (0.83, 0.63, 0.09)


def draw_header_bar(c, y):
    c.setFillColorRGB(*LEAF)
    c.rect(0, y, W, 6, fill=1, stroke=0)


def cover(c):
    # Fondo atmosférico
    c.setFillColorRGB(0.93, 0.96, 0.94)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColorRGB(*BARK)
    c.rect(0, H - 2.4 * inch, W, 2.4 * inch, fill=1, stroke=0)
    c.setFillColorRGB(*SUN)
    c.circle(W - 0.6 * inch, H - 0.5 * inch, 48, fill=1, stroke=0)
    c.setFillColorRGB(0.18, 0.42, 0.31)
    c.circle(0.4 * inch, H - 2.1 * inch, 70, fill=1, stroke=0)

    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_B, 12)
    c.drawString(MARGIN, H - 0.7 * inch, "UNIVERSIDAD GALILEO")
    c.setFont(FONT, 11)
    c.drawString(MARGIN, H - 0.95 * inch, "Facultad de Ingeniería de Sistemas, Informática y Ciencias de la Computación")
    c.drawString(MARGIN, H - 1.15 * inch, "Curso: Aplicaciones Móviles")

    c.setFont(FONT_B, 28)
    c.drawString(MARGIN, H - 1.8 * inch, "SeguritoApp")
    c.setFont(FONT, 13)
    c.drawString(MARGIN, H - 2.15 * inch, "Prototipo final y Guía de usabilidad")

    # Caja de datos
    c.setFillColorRGB(1, 1, 1)
    c.roundRect(MARGIN, 3.6 * inch, W - 2 * MARGIN, 3.2 * inch, 12, fill=1, stroke=0)
    c.setFillColorRGB(*BARK)
    c.setFont(FONT_B, 14)
    c.drawString(MARGIN + 18, 6.4 * inch, "Carátula · Datos del estudiante")
    c.setStrokeColorRGB(*LEAF)
    c.setLineWidth(1.5)
    c.line(MARGIN + 18, 6.25 * inch, W - MARGIN - 18, 6.25 * inch)

    rows = [
        ("Estudiante", "Otto Hernandez"),
        ("Carné", "08001620"),
        ("Actividad", "Actividad 2 · Prototipo SeguritoApp"),
        ("Problema", "Agencia de seguros El Gran Árbol"),
        ("Entregable", "Prototipo interactivo + Guía de usabilidad (PDF)"),
        ("Fecha", "9 de noviembre de 2026"),
    ]
    y = 5.85 * inch
    for label, value in rows:
        c.setFont(FONT, 10)
        c.setFillColorRGB(*MUTED)
        c.drawString(MARGIN + 18, y, label)
        c.setFont(FONT_B, 12)
        c.setFillColorRGB(*BARK)
        c.drawString(MARGIN + 140, y, value)
        y -= 0.35 * inch

    c.setFillColorRGB(*LEAF)
    c.roundRect(MARGIN, 1.3 * inch, W - 2 * MARGIN, 1.9 * inch, 12, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_B, 13)
    c.drawString(MARGIN + 18, 2.85 * inch, "Resumen del problema")
    c.setFont(FONT, 10)
    text = (
        "La agencia de seguros El Gran Árbol necesita una aplicación donde sus clientes "
        "consulten médicos, hospitales y laboratorios afiliados; soliciten autorización de "
        "medicamentos y hospitalización; y consulten el registro de solicitudes junto con "
        "notificaciones de aprobación o rechazo."
    )
    _text_block(c, text, MARGIN + 18, 2.55 * inch, W - 2 * MARGIN - 36, leading=14, fill=(1, 1, 1))

    c.setFillColorRGB(*MUTED)
    c.setFont(FONT, 9)
    c.drawCentredString(W / 2, 0.6 * inch, "Documento de entrega académica · Uso exclusivo del curso Aplicaciones Móviles")
    c.showPage()


def _text_block(c, text, x, y, max_w, leading=14, fill=(0.1, 0.14, 0.12), size=10):
    c.setFillColorRGB(*fill)
    c.setFont(FONT, size)
    words = text.split()
    line = ""
    for w in words:
        trial = (line + " " + w).strip()
        if c.stringWidth(trial, FONT, size) <= max_w:
            line = trial
        else:
            c.drawString(x, y, line)
            y -= leading
            line = w
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def page_title(c, title, subtitle=None):
    c.setFillColorRGB(0.96, 0.98, 0.97)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_header_bar(c, H - 0.35 * inch)
    c.setFillColorRGB(*BARK)
    c.setFont(FONT_B, 18)
    c.drawString(MARGIN, H - 0.85 * inch, title)
    if subtitle:
        c.setFont(FONT, 11)
        c.setFillColorRGB(*MUTED)
        c.drawString(MARGIN, H - 1.1 * inch, subtitle)
    c.setFont(FONT, 8)
    c.setFillColorRGB(*MUTED)
    c.drawRightString(W - MARGIN, 0.45 * inch, "SeguritoApp · Otto Hernandez · 08001620")


def section_intro(c):
    page_title(c, "1. Introducción", "Propósito de la guía de usabilidad")
    y = H - 1.5 * inch
    paragraphs = [
        "Esta guía describe cómo utilizar el prototipo SeguritoApp, pensado para clientes de la agencia de seguros El Gran Árbol. El objetivo es que un usuario sin capacitación previa pueda consultar la red afiliada, solicitar autorizaciones y dar seguimiento a las respuestas de la aseguradora.",
        "El prototipo prioriza claridad, jerarquía visual y un flujo corto: inicio de sesión → consulta o solicitud → registro → notificación. Cada pantalla cumple una sola tarea principal.",
        "La interfaz se diseñó en formato móvil (390 × 844 px, referencia iPhone 14/15) para simular el uso real en el teléfono del asegurado.",
    ]
    for p in paragraphs:
        y = _text_block(c, p, MARGIN, y, W - 2 * MARGIN, leading=15)
        y -= 10

    c.setFont(FONT_B, 12)
    c.setFillColorRGB(*BARK)
    c.drawString(MARGIN, y, "Objetivos de usabilidad")
    y -= 20
    goals = [
        "Localizar un afiliado (médico, hospital o laboratorio) en menos de 3 toques.",
        "Crear una solicitud de medicamento u hospitalización sin salir del flujo principal.",
        "Entender el estado de cada solicitud (en revisión, aprobada o rechazada) de un vistazo.",
        "Recibir y abrir notificaciones de aprobación o rechazo desde un acceso fijo.",
    ]
    for g in goals:
        c.setFillColorRGB(*LEAF)
        c.circle(MARGIN + 6, y + 3, 3, fill=1, stroke=0)
        y = _text_block(c, g, MARGIN + 18, y, W - 2 * MARGIN - 18, leading=14)
        y -= 6
    c.showPage()


def section_users(c):
    page_title(c, "2. Usuarios y escenarios", "A quién está dirigida la aplicación")
    y = H - 1.5 * inch
    y = _text_block(
        c,
        "Usuario primario: cliente asegurado de El Gran Árbol que necesita verificar cobertura de red y tramitar autorizaciones médicas desde el celular.",
        MARGIN,
        y,
        W - 2 * MARGIN,
        leading=15,
    )
    y -= 8
    scenarios = [
        ("Consultar red afiliada", "El usuario busca un pediatra cerca de Zona 9, revisa horario y teléfono, y confirma que está afiliado."),
        ("Autorizar medicamento", "El médico receta un fármaco; el cliente envía la solicitud y espera la notificación de aprobación o rechazo."),
        ("Autorizar hospitalización", "Se programa una internación; el cliente registra hospital, días y médico tratante."),
        ("Seguimiento", "Desde Solicitudes o Notificaciones abre el historial y ve el estado actualizado de cada folio."),
    ]
    for title, body in scenarios:
        c.setFillColorRGB(1, 1, 1)
        c.roundRect(MARGIN, y - 70, W - 2 * MARGIN, 78, 10, fill=1, stroke=0)
        c.setFillColorRGB(*BARK)
        c.setFont(FONT_B, 12)
        c.drawString(MARGIN + 14, y - 18, title)
        _text_block(c, body, MARGIN + 14, y - 38, W - 2 * MARGIN - 28, leading=13, fill=MUTED, size=10)
        y -= 92
    c.showPage()


def section_nav(c):
    page_title(c, "3. Estructura de navegación", "Mapa de pantallas del prototipo")
    y = H - 1.45 * inch
    y = _text_block(
        c,
        "La navegación inferior fija concentra las cuatro áreas críticas. Las altas (nueva solicitud) se abren desde Inicio o desde el botón “＋” en Solicitudes, manteniendo primero el listado y después el formulario.",
        MARGIN,
        y,
        W - 2 * MARGIN,
        leading=15,
    )
    y -= 16
    flow = SCREENS / "00_flujo.png"
    if flow.exists():
        img = ImageReader(str(flow))
        iw, ih = img.getSize()
        max_w = W - 2 * MARGIN
        max_h = 3.2 * inch
        scale = min(max_w / iw, max_h / ih)
        c.drawImage(img, MARGIN, y - ih * scale, iw * scale, ih * scale, mask="auto")
        y -= ih * scale + 18

    items = [
        ("Inicio", "Resumen de póliza, accesos a afiliados y nueva solicitud."),
        ("Afiliados", "Listado filtrable de médicos, hospitales y laboratorios."),
        ("Solicitudes", "Registro de autorizaciones con filtros por estado."),
        ("Avisos", "Notificaciones de envío, aprobación y rechazo."),
    ]
    for title, body in items:
        c.setFont(FONT_B, 11)
        c.setFillColorRGB(*LEAF)
        c.drawString(MARGIN, y, title)
        c.setFont(FONT, 10)
        c.setFillColorRGB(*MUTED)
        c.drawString(MARGIN + 90, y, body)
        y -= 18
    c.showPage()


def section_howto(c):
    page_title(c, "4. Guía paso a paso", "Cómo usar cada función principal")
    y = H - 1.45 * inch
    steps = [
        (
            "4.1 Iniciar sesión",
            [
                "Abre el prototipo y visualiza la pantalla de bienvenida de SeguritoApp.",
                "Ingresa correo y contraseña (campos vacíos; no hay credenciales precargadas).",
                "Pulsa Ingresar. Si falta un campo, el sistema muestra un mensaje de error claro.",
            ],
        ),
        (
            "4.2 Consultar afiliados",
            [
                "En Inicio elige Médicos, Hospitales o Laboratorios, o entra a la pestaña Afiliados.",
                "Usa los chips superiores para cambiar de categoría.",
                "Escribe en el buscador por nombre, especialidad o zona.",
                "Abre un resultado para ver teléfono, horario y estado de afiliación.",
            ],
        ),
        (
            "4.3 Solicitar autorización de medicamento",
            [
                "Desde Inicio → Nueva solicitud, o desde el detalle de un afiliado.",
                "Selecciona la pestaña Medicamento.",
                "Completa medicamento, detalle (dosis/cantidad) y médico tratante.",
                "Pulsa Enviar solicitud. Queda registrada en estado En revisión.",
            ],
        ),
        (
            "4.4 Solicitar autorización de hospitalización",
            [
                "En Nueva solicitud elige Hospitalización.",
                "Indica motivo/procedimiento, hospital o detalle de estancia y médico.",
                "Envía la solicitud; se agrega al registro y genera una notificación.",
            ],
        ),
        (
            "4.5 Registro y notificaciones",
            [
                "En Solicitudes filtra por Todas, En revisión, Aprobadas o Rechazadas.",
                "Abre un folio para ver timeline de seguimiento y notas de la aseguradora.",
                "En Avisos aparecen aprobaciones y rechazos; toca un aviso para ir al detalle.",
                "Usa ✓ para marcar todas las notificaciones como leídas.",
            ],
        ),
    ]
    for title, bullets in steps:
        if y < 1.8 * inch:
            c.showPage()
            page_title(c, "4. Guía paso a paso (cont.)", "Cómo usar cada función principal")
            y = H - 1.45 * inch
        c.setFont(FONT_B, 12)
        c.setFillColorRGB(*BARK)
        c.drawString(MARGIN, y, title)
        y -= 16
        for i, b in enumerate(bullets, 1):
            y = _text_block(c, f"{i}. {b}", MARGIN + 8, y, W - 2 * MARGIN - 8, leading=13, size=10)
            y -= 4
        y -= 10
    c.showPage()


def section_heuristics(c):
    page_title(c, "5. Criterios de usabilidad aplicados", "Heurísticas consideradas en el prototipo")
    y = H - 1.45 * inch
    items = [
        ("Visibilidad del estado", "Badges de En revisión / Aprobada / Rechazada y timeline en el detalle."),
        ("Correspondencia con el mundo real", "Lenguaje de seguros: póliza, afiliado, autorización, folio."),
        ("Control y libertad", "Botón volver, filtros, cerrar sesión y marcado de avisos leídos."),
        ("Consistencia", "Misma barra inferior, tipografía y color de marca en todas las pantallas."),
        ("Prevención de errores", "Validación de campos vacíos en login y en formularios de solicitud."),
        ("Reconocimiento", "Chips, iconos de categoría y accesos del inicio reducen memorización."),
        ("Flexibilidad", "Búsqueda y filtros para usuarios novatos y frecuentes."),
        ("Diseño minimalista", "Una tarea por pantalla; listado antes del formulario de alta."),
        ("Ayuda al error", "Mensajes breves cuando faltan datos o no hay resultados."),
        ("Documentación", "Esta guía y textos de apoyo dentro de los formularios."),
    ]
    for title, body in items:
        c.setFont(FONT_B, 10)
        c.setFillColorRGB(*LEAF)
        c.drawString(MARGIN, y, title)
        c.setFont(FONT, 10)
        c.setFillColorRGB(*MUTED)
        c.drawString(MARGIN + 150, y, body)
        y -= 22
    c.showPage()


def section_screens(c):
    page_title(c, "6. Pantallas del prototipo", "Referencias visuales para el archivo Figma")
    y = H - 1.4 * inch
    y = _text_block(
        c,
        "A continuación se muestran las pantallas clave del prototipo. En Figma cada imagen se coloca en un Frame de 390×844, se nombran según el flujo y se conectan en Prototype (tap → Navigate to).",
        MARGIN,
        y,
        W - 2 * MARGIN,
        leading=14,
    )
    y -= 12

    screens = [
        ("01_login.png", "Login"),
        ("02_home.png", "Inicio"),
        ("03_afiliados_medicos.png", "Afiliados"),
        ("05_nueva_medicamento.png", "Nueva solicitud"),
        ("06_solicitudes.png", "Registro"),
        ("08_notificaciones.png", "Notificaciones"),
    ]
    # 2 columnas x 3 filas
    col_w = (W - 2 * MARGIN - 16) / 2
    img_h = 2.55 * inch
    positions = []
    for i, (fname, label) in enumerate(screens):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + 16)
        yy = y - row * (img_h + 0.45 * inch)
        positions.append((x, yy, fname, label))

    for x, yy, fname, label in positions:
        path = SCREENS / fname
        c.setFont(FONT_B, 9)
        c.setFillColorRGB(*BARK)
        c.drawString(x, yy, label)
        if path.exists():
            img = ImageReader(str(path))
            c.drawImage(img, x, yy - img_h - 4, width=col_w * 0.72, height=img_h, preserveAspectRatio=True, mask="auto")
    c.showPage()


def section_figma(c):
    page_title(c, "7. Entrega del prototipo en Figma", "Cómo está organizado el archivo")
    y = H - 1.45 * inch
    paragraphs = [
        "El prototipo visual se entrega como archivo/proyecto Figma con frames móviles y conexiones de prototipo. Las pantallas fuente también viven en la carpeta assets/screens y el prototipo navegable en prototipo/index.html.",
        "Configuración recomendada en Figma: Device Frame iPhone 14/15 · 390×844 · Prototype connections On tap → Navigate to · Animation Instant o Dissolve 200ms.",
    ]
    for p in paragraphs:
        y = _text_block(c, p, MARGIN, y, W - 2 * MARGIN, leading=15)
        y -= 8

    c.setFont(FONT_B, 12)
    c.setFillColorRGB(*BARK)
    c.drawString(MARGIN, y, "Conexiones mínimas del Prototype")
    y -= 18
    links = [
        "Login → Inicio (botón Ingresar)",
        "Inicio → Afiliados / Nueva solicitud / Solicitudes / Notificaciones",
        "Afiliados → Detalle afiliado → Nueva solicitud",
        "Nueva solicitud → Detalle solicitud / Solicitudes",
        "Solicitudes → Detalle solicitud",
        "Notificaciones → Detalle solicitud",
        "Barra inferior: navegación global entre Inicio, Afiliados, Solicitudes y Avisos",
    ]
    for link in links:
        c.setFillColorRGB(*LEAF)
        c.circle(MARGIN + 5, y + 3, 2.5, fill=1, stroke=0)
        y = _text_block(c, link, MARGIN + 16, y, W - 2 * MARGIN - 16, leading=13, size=10)
        y -= 4

    y -= 12
    c.setFont(FONT_B, 12)
    c.setFillColorRGB(*BARK)
    c.drawString(MARGIN, y, "Criterios de aceptación del problema")
    y -= 18
    checks = [
        "Consulta de médicos, hospitales y laboratorios afiliados.",
        "Opciones para solicitar autorización de medicamentos.",
        "Opciones para solicitar autorización de hospitalización.",
        "Registro (historial) de las solicitudes.",
        "Notificaciones de aprobación o rechazo.",
    ]
    for ch in checks:
        c.setFont(FONT, 11)
        c.setFillColorRGB(*LEAF)
        c.drawString(MARGIN, y, "☑")
        c.setFillColorRGB(*BARK)
        c.drawString(MARGIN + 18, y, ch)
        y -= 18
    c.showPage()


def section_close(c):
    page_title(c, "8. Conclusión y evidencias", "Cierre de la entrega")
    y = H - 1.45 * inch
    y = _text_block(
        c,
        "SeguritoApp responde al problema de El Gran Árbol con un flujo móvil simple: el asegurado consulta la red afiliada, solicita autorizaciones de medicamento u hospitalización, consulta el registro y recibe notificaciones de aprobación o rechazo.",
        MARGIN,
        y,
        W - 2 * MARGIN,
        leading=15,
    )
    y -= 12
    y = _text_block(
        c,
        "La presente guía, junto con el prototipo interactivo y el archivo Figma, constituyen la entrega de la Actividad 2.",
        MARGIN,
        y,
        W - 2 * MARGIN,
        leading=15,
    )
    y -= 24
    c.setFillColorRGB(1, 1, 1)
    c.roundRect(MARGIN, y - 140, W - 2 * MARGIN, 150, 12, fill=1, stroke=0)
    c.setFillColorRGB(*BARK)
    c.setFont(FONT_B, 12)
    c.drawString(MARGIN + 16, y - 24, "Datos de identificación")
    c.setFont(FONT, 11)
    lines = [
        "Nombre: Otto Hernandez",
        "Carné: 08001620",
        "Curso: Aplicaciones Móviles · Actividad 2",
        "Producto: SeguritoApp · El Gran Árbol",
        "Fecha: 9 de noviembre de 2026",
    ]
    yy = y - 48
    for line in lines:
        c.drawString(MARGIN + 16, yy, line)
        yy -= 18

    c.setFillColorRGB(*MUTED)
    c.setFont(FONT, 9)
    c.drawCentredString(W / 2, 0.7 * inch, "Fin del documento")
    c.showPage()


def main():
    c = canvas.Canvas(str(OUT), pagesize=letter)
    c.setTitle("Guía de usabilidad SeguritoApp - Otto Hernandez 08001620")
    c.setAuthor("Otto Hernandez")
    c.setSubject("Actividad 2 Aplicaciones Móviles - SeguritoApp")
    cover(c)
    section_intro(c)
    section_users(c)
    section_nav(c)
    section_howto(c)
    section_heuristics(c)
    section_screens(c)
    section_figma(c)
    section_close(c)
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
