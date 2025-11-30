from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from textwrap import wrap
from io import BytesIO
import os
from reportes.utils_pdf import start_pdf, finish_pdf, draw_footer


def rd(monto):
    """Formatea montos a pesos dominicanos"""
    try:
        return f"RD$ {monto:,.2f}"
    except:
        return "RD$ 0.00"


def solo_monto(monto):
    """Formatea solo el número sin símbolo de moneda"""
    try:
        return f"{monto:,.2f}"
    except:
        return "0.00"


def numero_a_letras(numero):
    """
    Convierte un número a letras (implementación básica)
    Para producción, usar una librería como 'num2words'
    """
    try:
        # Instalar con: pip install num2words
        from num2words import num2words

        entero = int(numero)
        decimales = int((numero - entero) * 100)
        texto = num2words(entero, lang="es").upper()
        return f"{texto} PESOS CON {decimales:02d}/100"
    except ImportError:
        # Fallback si no está instalada la librería
        return f"***{numero:,.2f}***"


def validar_datos_factura(factura, cliente, detalles):
    """Valida que los datos de la factura sean correctos"""
    errores = []

    if not detalles or len(detalles) == 0:
        errores.append("La factura no tiene detalles")

    if factura.total <= 0:
        errores.append("El total de la factura debe ser mayor a cero")

    # Validar que los subtotales cuadren
    subtotal_calculado = sum(d.subtotal for d in detalles)
    if abs(subtotal_calculado - factura.subtotal) > 0.01:
        errores.append("Los subtotales no coinciden")

    return errores


def generar_pdf_factura(factura, cliente, detalles, empresa_info=None):
    """
    Genera PDF de factura con validaciones y diseño mejorado

    Args:
        factura: Objeto Factura
        cliente: Objeto Cliente (puede ser None)
        detalles: QuerySet de DetalleFactura
        empresa_info: Dict con info de la empresa (opcional)
            {
                'nombre': 'Mi Empresa',
                'rnc': '000-0000000-0',
                'direccion': 'Calle Principal #123',
                'telefono': '809-000-0000',
                'email': 'info@miempresa.com'
            }
    """
    # --- VALIDACIONES ---
    errores = validar_datos_factura(factura, cliente, detalles)
    if errores:
        raise ValueError(f"Errores en la factura: {', '.join(errores)}")

    # --- CONFIG ---
    TOP_MARGIN = 10 * mm
    LEFT_MARGIN = 5 * mm
    RIGHT_MARGIN = 5 * mm
    TICKET_WIDTH = 80 * mm
    BASE_HEIGHT = 180 * mm  # Aumentado para info adicional
    DETAIL_HEIGHT = 3 * mm
    MAX_NAME_CHARS = 22

    # Calcular altura según cantidad de detalles
    lines = 0
    for d in detalles:
        lines += len(wrap(d.producto.nombre, MAX_NAME_CHARS))
        lines += 1  # cantidad/precio/subtotal

    total_height = BASE_HEIGHT + (lines * DETAIL_HEIGHT)

    # Crear PDF
    p, buffer = start_pdf((TICKET_WIDTH, total_height))
    x_center = TICKET_WIDTH / 2
    y = total_height - TOP_MARGIN

    # --- LOGO Y ENCABEZADO EMPRESA ---
    logo_path = "static/logo.webp"
    if os.path.exists(logo_path):
        p.drawImage(
            ImageReader(logo_path),
            LEFT_MARGIN,
            y - 35,
            width=40,
            height=40,
            preserveAspectRatio=True,
            mask="auto",
        )

    # Info de la empresa
    p.setFont("Helvetica-Bold", 8)
    if empresa_info:
        p.drawCentredString(x_center, y - 10, empresa_info.get("nombre", "Mi Empresa"))
        y -= 12
        p.setFont("Helvetica", 6)
        if empresa_info.get("rnc"):
            p.drawCentredString(x_center, y, f"RNC: {empresa_info['rnc']}")
            y -= 8
        if empresa_info.get("telefono"):
            p.drawCentredString(x_center, y, f"Tel: {empresa_info['telefono']}")
            y -= 8
    else:
        y -= 45

    y -= 8

    # Línea separadora con más espacio
    p.setStrokeColor(colors.grey)
    p.line(LEFT_MARGIN, y, TICKET_WIDTH - RIGHT_MARGIN, y)
    y -= 14

    # --- TÍTULO FACTURA ---
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(x_center, y, "FACTURA DE VENTA")
    y -= 18

    # --- NUMERO Y FECHA ---
    p.setFont("Helvetica-Bold", 9)
    p.drawCentredString(x_center, y, f"No. {factura.numero_factura}")
    y -= 12

    p.setFont("Helvetica", 8)
    p.drawCentredString(x_center, y, factura.fecha.strftime("%d/%m/%Y – %H:%M"))
    y -= 16

    # Línea separadora con más espacio
    p.line(LEFT_MARGIN, y, TICKET_WIDTH - RIGHT_MARGIN, y)
    y -= 14

    # --- INFORMACIÓN DEL CLIENTE ---
    p.setFont("Helvetica-Bold", 8)
    p.drawString(LEFT_MARGIN, y, "CLIENTE:")
    y -= 10

    p.setFont("Helvetica", 7.5)
    if cliente:
        # Wrap del nombre si es muy largo
        nombre_lines = wrap(cliente.nombre, 30)
        for line in nombre_lines:
            p.drawString(LEFT_MARGIN, y, line)
            y -= 9

        if cliente.rnc_cedula:
            p.drawString(LEFT_MARGIN, y, f"RNC/Cédula: {cliente.rnc_cedula}")
            y -= 9

        if cliente.telefono:
            p.drawString(LEFT_MARGIN, y, f"Tel: {cliente.telefono}")
            y -= 9

        if cliente.direccion:
            dir_lines = wrap(cliente.direccion, 30)
            for line in dir_lines:
                p.drawString(LEFT_MARGIN, y, line)
                y -= 9
    else:
        p.drawString(LEFT_MARGIN, y, factura.nombre_cliente or "Cliente General")
        y -= 9

    y -= 6

    # Línea separadora
    p.line(LEFT_MARGIN, y, TICKET_WIDTH - RIGHT_MARGIN, y)
    y -= 12

    # --- ENCABEZADO DE TABLA ---
    p.setFont("Helvetica-Bold", 7.5)
    p.drawString(LEFT_MARGIN, y, "Producto")
    p.drawCentredString(108, y, "Cant")
    p.drawRightString(155, y, "Precio")
    p.drawRightString(TICKET_WIDTH - RIGHT_MARGIN, y, "Total")
    y -= 12

    # Línea debajo del encabezado
    p.setLineWidth(0.5)
    p.line(LEFT_MARGIN, y, TICKET_WIDTH - RIGHT_MARGIN, y)
    y -= 10

    # --- DETALLES ---
    p.setFont("Helvetica", 7)
    NAME_COL = LEFT_MARGIN
    QTY_COL = 108
    PRICE_RIGHT = 155
    SUBTOTAL_RIGHT = TICKET_WIDTH - RIGHT_MARGIN

    for idx, d in enumerate(detalles, 1):
        # Nombre del producto (con wrap)
        nombre_wrap = wrap(d.producto.nombre, MAX_NAME_CHARS)
        start_y = y

        for line in nombre_wrap:
            p.drawString(NAME_COL, y, line)
            y -= DETAIL_HEIGHT

        # Cantidad, precio y subtotal en la primera línea del producto
        p.drawCentredString(QTY_COL, start_y, f"{d.cantidad}")
        p.drawRightString(PRICE_RIGHT, start_y, solo_monto(d.precio_unitario))
        p.drawRightString(SUBTOTAL_RIGHT, start_y, solo_monto(d.subtotal))

        y -= 4  # Espacio entre productos

    y -= 10

    # Línea antes de totales
    p.setLineWidth(0.5)
    p.line(LEFT_MARGIN, y, TICKET_WIDTH - RIGHT_MARGIN, y)
    y -= 14

    # --- TOTALES ---
    RIGHT_COL = TICKET_WIDTH - RIGHT_MARGIN
    LABEL_COL = RIGHT_COL - 40 * mm

    p.setFont("Helvetica", 8)
    p.drawString(LABEL_COL, y, "Subtotal:")
    p.drawRightString(RIGHT_COL, y, rd(factura.subtotal))
    y -= 10

    p.drawString(LABEL_COL, y, "ITBIS (18%):")
    p.drawRightString(RIGHT_COL, y, rd(factura.itbis))
    y -= 12

    # Línea antes del total con más espacio
    p.setLineWidth(1)
    p.line(LABEL_COL - 5, y, RIGHT_COL, y)
    y -= 10

    p.setFont("Helvetica-Bold", 9)
    p.drawString(LABEL_COL, y, "TOTAL:")
    p.drawRightString(RIGHT_COL, y, rd(factura.total))
    y -= 14

    # Total en letras
    p.setFont("Helvetica", 6)
    total_letras = numero_a_letras(factura.total)
    # Wrap del total en letras si es muy largo
    letras_lines = wrap(total_letras, 35)
    for line in letras_lines:
        p.drawCentredString(x_center, y, line)
        y -= 8

    y -= 8

    # --- INFORMACIÓN ADICIONAL ---
    p.setFont("Helvetica", 7)
    p.drawString(LEFT_MARGIN, y, f"Método de pago: {factura.metodo_pago}")
    y -= 10

    # Línea separadora
    p.line(LEFT_MARGIN, y, TICKET_WIDTH - RIGHT_MARGIN, y)
    y -= 10

    # Mensaje de agradecimiento
    p.setFont("Helvetica-Bold", 7)
    p.drawCentredString(x_center, y, "¡GRACIAS POR SU COMPRA!")
    y -= 8

    p.setFont("Helvetica", 6)
    if empresa_info and empresa_info.get("email"):
        p.drawCentredString(x_center, y, empresa_info["email"])

    # --- FOOTER ---
    draw_footer(p, TICKET_WIDTH, "Documento generado automáticamente")

    return finish_pdf(p, buffer)
