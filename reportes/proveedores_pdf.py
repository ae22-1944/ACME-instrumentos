from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportes.base_reporte import dibujar_tabla_con_paginacion


def _ultima_entrega(proveedor):
    """Obtiene la fecha de la última entrega del proveedor"""
    producto = proveedor.productos.order_by("-creado_en").first()
    return producto.creado_en.strftime("%d/%m/%Y %H:%M") if producto else "N/A"


def generar_pdf_proveedores(proveedores):
    """
    Genera PDF de reporte de proveedores con paginación automática
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Título del reporte
    titulo = "Reporte de Proveedores"

    # Headers de la tabla
    headers = [
        "Nombre",
        "RNC/Cédula",
        "Teléfono",
        "Contacto",
        "Correo",
        "Última Entrega",
        "Estado",
    ]

    # Construir filas
    rows = [
        [
            prov.nombre,
            prov.rnc_cedula,
            prov.telefono,
            prov.contacto or "",
            prov.correo,
            _ultima_entrega(prov),
            prov.estado,
        ]
        for prov in proveedores
    ]

    # Dibujar tabla con paginación automática
    dibujar_tabla_con_paginacion(p, titulo, headers, rows)

    # Guardar y retornar
    p.save()
    buffer.seek(0)
    return buffer
