#!/usr/bin/env python3
"""PDF de evidencia - Actividad 3 DivisApp 08001620."""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "Evidencia_Actividad3_DivisApp_OttoHernandez_08001620.pdf"
SCREEN = ROOT / "assets" / "pantallazo_DivisApp_08001620.png"
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
PRIMARY = (0.15, 0.35, 0.72)
DARK = (0.10, 0.14, 0.22)
MUTED = (0.40, 0.45, 0.52)
REPO = "https://github.com/Ottogt/Desarrollo-de-Aplicaciones-"
APK_PATH = "entregables/DivisApp_08001620.apk"


def cover(c: canvas.Canvas) -> None:
    c.setFillColorRGB(0.94, 0.96, 0.99)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColorRGB(*PRIMARY)
    c.rect(0, H - 2.5 * inch, W, 2.5 * inch, fill=1, stroke=0)

    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_B, 12)
    c.drawString(MARGIN, H - 0.7 * inch, "UNIVERSIDAD GALILEO")
    c.setFont(FONT, 10)
    c.drawString(
        MARGIN,
        H - 0.95 * inch,
        "Facultad de Ingeniería de Sistemas, Informática y Ciencias de la Computación",
    )
    c.drawString(MARGIN, H - 1.15 * inch, "Curso: Aplicaciones Móviles")

    c.setFont(FONT_B, 28)
    c.drawString(MARGIN, H - 1.85 * inch, "DivisApp 08001620")
    c.setFont(FONT, 13)
    c.drawString(MARGIN, H - 2.2 * inch, "Conversor de divisas · Ionic Framework")

    c.setFillColorRGB(1, 1, 1)
    c.roundRect(MARGIN, 3.5 * inch, W - 2 * MARGIN, 3.4 * inch, 12, fill=1, stroke=0)
    c.setFillColorRGB(*DARK)
    c.setFont(FONT_B, 14)
    c.drawString(MARGIN + 18, 6.5 * inch, "Carátula · Datos del estudiante")
    c.setStrokeColorRGB(*PRIMARY)
    c.setLineWidth(1.5)
    c.line(MARGIN + 18, 6.35 * inch, W - MARGIN - 18, 6.35 * inch)

    rows = [
        ("Estudiante", "Otto Hernandez"),
        ("Carné", "08001620"),
        ("Actividad", "Actividad 3 · Conversor de divisas"),
        ("Framework", "Ionic + Angular + Capacitor"),
        ("Tasa", "8 quetzales = 1 dólar"),
        ("Fecha", "16 de noviembre de 2026"),
    ]
    y = 5.95 * inch
    for label, value in rows:
        c.setFont(FONT, 10)
        c.setFillColorRGB(*MUTED)
        c.drawString(MARGIN + 18, y, label)
        c.setFont(FONT_B, 12)
        c.setFillColorRGB(*DARK)
        c.drawString(MARGIN + 140, y, value)
        y -= 0.35 * inch

    c.setFillColorRGB(*PRIMARY)
    c.roundRect(MARGIN, 1.2 * inch, W - 2 * MARGIN, 1.9 * inch, 12, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_B, 13)
    c.drawString(MARGIN + 18, 2.7 * inch, "Contenido del documento")
    c.setFont(FONT, 10)
    items = [
        "1. Carátula con datos del estudiante",
        "2. Pantallazo de la app con carné en quetzales y equivalente en dólares",
        "3. URL del repositorio público de GitHub",
        "4. Referencia al APK generado del proyecto",
    ]
    y = 2.35 * inch
    for item in items:
        c.drawString(MARGIN + 18, y, item)
        y -= 0.28 * inch

    c.showPage()


def screenshot_page(c: canvas.Canvas) -> None:
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColorRGB(*PRIMARY)
    c.rect(0, H - 0.9 * inch, W, 0.9 * inch, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_B, 14)
    c.drawString(MARGIN, H - 0.55 * inch, "Pantallazo del proyecto · DivisApp 08001620")

    c.setFillColorRGB(*DARK)
    c.setFont(FONT_B, 12)
    c.drawString(MARGIN, H - 1.35 * inch, "Evidencia de conversión")
    c.setFont(FONT, 10)
    c.setFillColorRGB(*MUTED)
    lines = [
        "Se ingresó el número de carné como cantidad en quetzales:",
        "  8,001,620 GTQ  (carné 08001620)",
        "Con tasa fija 8 GTQ = 1 USD, el equivalente mostrado es:",
        "  1,000,202.50 USD",
    ]
    y = H - 1.7 * inch
    for line in lines:
        c.drawString(MARGIN, y, line)
        y -= 0.28 * inch

    if SCREEN.exists():
        img = ImageReader(str(SCREEN))
        iw, ih = img.getSize()
        max_w = W - 2 * MARGIN
        max_h = 5.8 * inch
        scale = min(max_w / iw, max_h / ih)
        dw, dh = iw * scale, ih * scale
        x = (W - dw) / 2
        c.drawImage(img, x, 0.7 * inch, width=dw, height=dh, preserveAspectRatio=True, mask="auto")
    else:
        c.setFillColorRGB(0.8, 0.2, 0.2)
        c.drawString(MARGIN, 4 * inch, "No se encontró el pantallazo en assets/")

    c.setFillColorRGB(*MUTED)
    c.setFont(FONT, 8)
    c.drawRightString(W - MARGIN, 0.4 * inch, "Otto Hernandez · 08001620")
    c.showPage()


def repo_and_apk_page(c: canvas.Canvas) -> None:
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColorRGB(*PRIMARY)
    c.rect(0, H - 0.9 * inch, W, 0.9 * inch, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont(FONT_B, 14)
    c.drawString(MARGIN, H - 0.55 * inch, "Repositorio GitHub y APK")

    c.setFillColorRGB(*DARK)
    c.setFont(FONT_B, 13)
    c.drawString(MARGIN, H - 1.5 * inch, "1. URL del repositorio público")
    c.setFont(FONT, 10)
    c.setFillColorRGB(*MUTED)
    c.drawString(MARGIN, H - 1.85 * inch, "Código fuente de la aplicación Ionic:")
    c.setFillColorRGB(*PRIMARY)
    c.setFont(FONT_B, 11)
    c.drawString(MARGIN, H - 2.2 * inch, REPO)

    c.setFillColorRGB(0.94, 0.96, 0.99)
    c.roundRect(MARGIN, H - 4.5 * inch, W - 2 * MARGIN, 1.9 * inch, 10, fill=1, stroke=0)
    c.setFillColorRGB(*DARK)
    c.setFont(FONT_B, 12)
    c.drawString(MARGIN + 16, H - 2.85 * inch, "Ubicación en el repositorio")
    c.setFont(FONT, 10)
    c.setFillColorRGB(*MUTED)
    repo_lines = [
        "Carpeta: Actividad 3/",
        "Proyecto Ionic: Actividad 3/conversor-de-divisas/",
        "APK: Actividad 3/entregables/DivisApp_08001620.apk",
        "PDF: Actividad 3/docs/Evidencia_Actividad3_DivisApp_OttoHernandez_08001620.pdf",
    ]
    y = H - 3.2 * inch
    for line in repo_lines:
        c.drawString(MARGIN + 16, y, line)
        y -= 0.28 * inch

    c.setFillColorRGB(*DARK)
    c.setFont(FONT_B, 13)
    c.drawString(MARGIN, H - 5.0 * inch, "2. APK generado del proyecto")
    c.setFont(FONT, 10)
    c.setFillColorRGB(*MUTED)
    apk_lines = [
        "Se generó el APK de depuración con Capacitor + Gradle:",
        f"  Archivo adjunto / entregable: {APK_PATH}",
        "  Nombre: DivisApp_08001620.apk",
        "  Plataforma: Android (debug)",
        "  App ID: gt.edu.galileo.divisapp08001620",
        "  Título de la app: DivisApp 08001620",
        "",
        "El APK se incluye junto a este PDF en la carpeta Actividad 3",
        "del repositorio (apartado de entregables de la tarea).",
    ]
    y = H - 5.4 * inch
    for line in apk_lines:
        c.drawString(MARGIN, y, line)
        y -= 0.28 * inch

    c.setFillColorRGB(*MUTED)
    c.setFont(FONT, 8)
    c.drawRightString(W - MARGIN, 0.4 * inch, "Otto Hernandez · 08001620")
    c.showPage()


def main() -> None:
    c = canvas.Canvas(str(OUT), pagesize=letter)
    c.setTitle("Evidencia Actividad 3 - DivisApp 08001620")
    c.setAuthor("Otto Hernandez")
    cover(c)
    screenshot_page(c)
    repo_and_apk_page(c)
    c.save()
    print(f"PDF generado: {OUT}")


if __name__ == "__main__":
    main()
