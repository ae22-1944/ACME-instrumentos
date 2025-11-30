from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm

DEFAULT_PAGE = letter

TOP_MARGIN = 20 * mm
LEFT_MARGIN = 10 * mm
RIGHT_MARGIN = 10 * mm
BOTTOM_MARGIN = 15 * mm

FONT_TITLE = ("Helvetica-Bold", 16)
FONT_SUBTITLE = ("Helvetica-Bold", 10)
FONT_NORMAL = ("Helvetica", 9)


def draw_header(p, titulo, subtitulo=None):
    p.setFont(*FONT_TITLE)
    p.drawString(LEFT_MARGIN, 800, "ACME Instrumentos")

    p.setFont(*FONT_SUBTITLE)
    p.drawString(LEFT_MARGIN, 785, titulo)

    if subtitulo:
        p.setFont(*FONT_NORMAL)
        p.drawString(LEFT_MARGIN, 770, subtitulo)

    # línea horizontal
    p.line(LEFT_MARGIN, 760, 590, 760)

    return 750  # posición inicial sugerida para contenido


def draw_footer(
    p, page_width, text="Sistema ACME – Documento generado automáticamente"
):
    p.setFont("Helvetica", 7)
    p.drawCentredString(page_width / 2, 10, text)


def start_pdf(page_size=DEFAULT_PAGE):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=page_size)
    return p, buffer


def finish_pdf(p, buffer):
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
