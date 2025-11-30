from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportes.base_reporte import dibujar_tabla_con_paginacion
from facturacion.models import Factura


def _ultima_compra(cliente):
    """Obtiene la fecha de la última compra del cliente"""
    factura = Factura.objects.filter(cliente=cliente).order_by("-fecha").first()
    return factura.fecha.strftime("%d/%m/%Y %H:%M") if factura else "N/A"


def generar_pdf_clientes(clientes):
    """
    Genera PDF de reporte de clientes con paginación automática
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Título del reporte
    titulo = "Reporte de Clientes"

    # Headers de la tabla
    headers = ["Nombre", "RNC/Cédula", "Teléfono", "Correo", "Última Compra", "Estado"]

    # Construir filas
    rows = [
        [
            c.nombre,
            c.rnc_cedula,
            c.telefono,
            c.correo,
            _ultima_compra(c),
            c.estado,
        ]
        for c in clientes
    ]

    # Dibujar tabla con paginación automática
    dibujar_tabla_con_paginacion(p, titulo, headers, rows)

    # Guardar y retornar
    p.save()
    buffer.seek(0)
    return buffer
