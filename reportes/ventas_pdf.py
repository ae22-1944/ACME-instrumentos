from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportes.base_reporte import dibujar_tabla_con_paginacion
from django.db.models import Sum


def generar_pdf_ventas(ventas, fecha_inicio, fecha_fin):
    """
    Genera PDF de reporte de ventas con paginación automática
    Incluye rango de fechas y total general
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Título con rango de fechas
    titulo = f"Reporte de Ventas (Del {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')})"

    # Headers de la tabla
    headers = ["ID Venta", "Fecha", "Cliente", "Total Venta"]

    rows = []
    total_general = 0

    # Llenar filas y calcular el total general
    for v in ventas:
        rows.append(
            [
                v.numero_factura,
                v.fecha.strftime("%d/%m/%Y"),
                v.cliente,
                f"RD${v.total:,.2f}",
            ]
        )
        total_general += v.total

    # Texto del total para mostrar al final
    texto_total = f"TOTAL DE VENTAS: RD${total_general:,.2f}"

    # Dibujar tabla con paginación automática
    dibujar_tabla_con_paginacion(p, titulo, headers, rows, texto_total=texto_total)

    # Guardar y retornar
    p.save()
    buffer.seek(0)
    return buffer
