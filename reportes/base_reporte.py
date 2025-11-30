from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from datetime import datetime
import os
from reportlab.platypus import Table, TableStyle

LOGO_PATH = "static/logo.webp"

# Configuración de márgenes y espaciado
MARGEN_SUPERIOR = 40
MARGEN_INFERIOR = 50
MARGEN_IZQUIERDO = 25
MARGEN_DERECHO = 25
LOGO_MARGEN_Y = 15  # Margen adicional entre logo y encabezado


def crear_encabezado(p, titulo, page_number=1, total_pages=None):
    """
    Crea el encabezado con logo, título y número de página
    """
    page_width, page_height = letter
    margen_superior_pos = page_height - MARGEN_SUPERIOR

    # Logo con margen mejorado
    if os.path.exists(LOGO_PATH):
        logo_y = margen_superior_pos - 60 - LOGO_MARGEN_Y
        p.drawImage(
            ImageReader(LOGO_PATH),
            MARGEN_IZQUIERDO,
            logo_y,
            width=85,
            height=85,
            preserveAspectRatio=True,
            mask="auto",
        )

    # Título centrado
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(page_width / 2, margen_superior_pos, titulo)

    # Fecha debajo del título
    now = datetime.now().strftime("%d/%m/%Y – %H:%M")
    p.setFont("Helvetica", 11)
    p.drawCentredString(page_width / 2, margen_superior_pos - 18, f"Generado el {now}")

    # Número de página en la esquina superior derecha
    p.setFont("Helvetica", 9)
    if total_pages:
        p.drawRightString(
            page_width - MARGEN_DERECHO,
            margen_superior_pos,
            f"Página {page_number} de {total_pages}",
        )
    else:
        p.drawRightString(
            page_width - MARGEN_DERECHO, margen_superior_pos, f"Página {page_number}"
        )

    # Retornar la posición Y donde comienza el contenido
    return margen_superior_pos - 90 - LOGO_MARGEN_Y


def crear_pie_pagina(p, page_number, total_pages=None):
    """
    Crea el pie de página con número de página centrado
    """
    page_width, page_height = letter
    p.setFont("Helvetica", 9)

    if total_pages:
        texto = f"Página {page_number} de {total_pages}"
    else:
        texto = f"Página {page_number}"

    p.drawCentredString(page_width / 2, MARGEN_INFERIOR - 30, texto)


def dividir_tabla_en_paginas(
    headers, rows, altura_disponible_primera, altura_disponible_otras
):
    """
    Divide las filas de la tabla en páginas según el espacio disponible

    Returns:
        Lista de tuplas (headers, rows_pagina)
    """
    ALTURA_FILA = 20  # Altura aproximada por fila (ajusta según tu fuente)
    ALTURA_HEADER = 25

    paginas = []

    # Primera página
    filas_primera_pagina = int(
        (altura_disponible_primera - ALTURA_HEADER) / ALTURA_FILA
    )
    if filas_primera_pagina > 0:
        paginas.append((headers, rows[:filas_primera_pagina]))
        rows_restantes = rows[filas_primera_pagina:]
    else:
        rows_restantes = rows

    # Páginas siguientes
    filas_por_pagina = int((altura_disponible_otras - ALTURA_HEADER) / ALTURA_FILA)

    while rows_restantes:
        paginas.append((headers, rows_restantes[:filas_por_pagina]))
        rows_restantes = rows_restantes[filas_por_pagina:]

    return paginas


def dibujar_tabla_dinamica(p, headers, rows, start_y, es_primera_pagina=True):
    """
    Dibuja una tabla dinámica con anchos calculados automáticamente

    Returns:
        y_final: posición Y donde termina la tabla
    """
    page_width, page_height = letter
    max_width = page_width - MARGEN_IZQUIERDO - MARGEN_DERECHO
    FONT_SIZE = 8

    # --- 1. Calcular anchos MÍNIMOS basados en el contenido ---
    col_widths = [p.stringWidth(h, "Helvetica-Bold", 9) + 10 for h in headers]

    for row in rows:
        for i, cell in enumerate(row):
            w = p.stringWidth(str(cell), "Helvetica", FONT_SIZE) + 10
            col_widths[i] = max(col_widths[i], w)

    total_min_width = sum(col_widths)

    # --- 2. Distribuir el espacio sobrante ---
    if total_min_width < max_width:
        sobrante = max_width - total_min_width
        num_cols = len(headers)
        adicional_por_columna = sobrante / num_cols
        col_width_list = [w + adicional_por_columna for w in col_widths]
    else:
        scale = max_width / total_min_width
        col_width_list = [w * scale for w in col_widths]

    # --- 3. Crear estilos con zebra stripes ---
    data = [headers] + rows

    table_style = [
        # Headers
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4A4A4A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        # Contenido
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), FONT_SIZE),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]

    # Zebra stripes alternados
    for i in range(1, len(data)):
        if i % 2 == 0:
            table_style.append(
                ("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F5F5F5"))
            )

    table = Table(data, colWidths=col_width_list)
    table.setStyle(TableStyle(table_style))

    # Calcular posición
    width, height = table.wrapOn(p, max_width, page_height)
    x = MARGEN_IZQUIERDO
    y = start_y - height

    table.drawOn(p, x, y)

    return y


def dibujar_tabla_con_paginacion(p, titulo, headers, rows, texto_total=None):
    """
    Dibuja una tabla con paginación automática

    Args:
        p: Canvas de ReportLab
        titulo: Título del reporte
        headers: Lista de encabezados
        rows: Lista de filas
        texto_total: Texto opcional para mostrar al final (ej: "TOTAL: $1000")

    Returns:
        Número total de páginas creadas
    """
    page_width, page_height = letter

    # Calcular alturas disponibles
    altura_disponible_primera = page_height - MARGEN_SUPERIOR - MARGEN_INFERIOR - 120
    altura_disponible_otras = page_height - MARGEN_SUPERIOR - MARGEN_INFERIOR - 90

    # Dividir tabla en páginas
    paginas = dividir_tabla_en_paginas(
        headers, rows, altura_disponible_primera, altura_disponible_otras
    )
    total_pages = len(paginas)

    # Dibujar cada página
    for num_pagina, (headers_pag, rows_pag) in enumerate(paginas, start=1):
        if num_pagina > 1:
            p.showPage()  # Nueva página

        # Encabezado
        y = crear_encabezado(p, titulo, num_pagina, total_pages)

        # Tabla
        y = dibujar_tabla_dinamica(
            p, headers_pag, rows_pag, y, es_primera_pagina=(num_pagina == 1)
        )

        # Pie de página
        crear_pie_pagina(p, num_pagina, total_pages)

        # Texto total solo en la última página
        if texto_total and num_pagina == total_pages:
            p.setFont("Helvetica-Bold", 11)
            p.drawRightString(page_width - MARGEN_DERECHO, y - 25, texto_total)

    return total_pages
