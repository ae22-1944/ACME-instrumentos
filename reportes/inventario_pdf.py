from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportes.base_reporte import dibujar_tabla_con_paginacion


def generar_pdf_inventario(productos):
    """
    Ejemplo para reporte de inventario con paginación
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    titulo = "Reporte de Inventario"
    headers = ["Código", "Producto", "Categoría", "Stock", "Precio"]
    rows = []

    for prod in productos:
        rows.append(
            [
                prod.codigo,
                prod.nombre,
                prod.categoria.descripcion if prod.categoria else "N/A",
                str(prod.stock_actual),
                f"RD${prod.precio_unitario:,.2f}",
            ]
        )

    # Sin texto total en este caso
    dibujar_tabla_con_paginacion(p, titulo, headers, rows)

    p.save()
    buffer.seek(0)

    return buffer
