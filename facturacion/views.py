import json
from decimal import Decimal, ROUND_HALF_UP
from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction
from django.contrib import messages
from django.http import FileResponse
from django.db.models import Sum
from .utils import generar_pdf_factura
from datetime import datetime, date

from .forms import FacturaForm, ProductoEnFacturaForm
from inventario.models import Producto
from .models import Factura, DetalleFactura
from clientes.models import Cliente
from reportes.ventas_pdf import generar_pdf_ventas

ITBIS_RATE = Decimal("0.18")


def crear_factura(request):
    print("POST DATA:", request.POST)

    clientes_qs = Cliente.objects.filter(estado="activo")
    productos_qs = Producto.objects.filter(stock_actual__gte=1).order_by("nombre")

    if request.method == "POST":
        factura_form = FacturaForm(request.POST, clientes_qs=clientes_qs)
        producto_form = ProductoEnFacturaForm(request.POST, productos_qs=productos_qs)

        # Items enviados desde el input hidden
        items_json = request.POST.get("items", "[]")
        try:
            items = json.loads(items_json)
        except json.JSONDecodeError:
            items = []

        # Validación mínima
        if not items:
            messages.error(request, "Debe agregar al menos un producto a la factura.")
            return render(
                request,
                "factura_form.html",
                {
                    "factura_form": factura_form,
                    "producto_form": producto_form,
                    "productos": productos_qs,
                },
            )

        if factura_form.is_valid():
            with transaction.atomic():
                # Creamos la factura preliminar
                factura = factura_form.save(commit=False)

                subtotal = Decimal("0.00")
                detalles_a_crear = []

                # VALIDACIÓN DE STOCK + cálculo de totales
                for it in items:
                    prod_id = it.get("producto_id")
                    cantidad = int(it.get("cantidad", 0))

                    if not prod_id or prod_id in ["", "0"] or cantidad <= 0:
                        continue

                    # Lock de fila para evitar inconsistencia si dos facturan a la vez
                    producto = Producto.objects.select_for_update().get(pk=prod_id)

                    # VALIDAR STOCK ANTES DE VENDER
                    if producto.stock_actual < cantidad:
                        raise ValueError(
                            f"No hay suficiente stock de {producto.nombre}. "
                            f"Disponible: {producto.stock_actual}, solicitado: {cantidad}"
                        )

                    precio_unit = producto.precio_unitario
                    linea_subtotal = (precio_unit * Decimal(cantidad)).quantize(
                        Decimal("0.01"), rounding=ROUND_HALF_UP
                    )

                    subtotal += linea_subtotal

                    detalles_a_crear.append(
                        {
                            "producto": producto,
                            "cantidad": cantidad,
                            "precio_unitario": precio_unit,
                            "subtotal": linea_subtotal,
                        }
                    )

                # Calcular impuestos y total
                itbis = (subtotal * ITBIS_RATE).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
                total = (subtotal + itbis).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )

                factura.subtotal = subtotal
                factura.itbis = itbis
                factura.total = total
                factura.save()  # Genera número de factura si tu modelo lo hace

                # Crear detalles y actualizar stock
                for det in detalles_a_crear:
                    DetalleFactura.objects.create(
                        factura=factura,
                        producto=det["producto"],
                        cantidad=det["cantidad"],
                        precio_unitario=det["precio_unitario"],
                        subtotal=det["subtotal"],
                    )

                    # Reducir stock
                    producto = det["producto"]
                    producto.stock_actual -= det["cantidad"]
                    producto.save()

            cliente = factura.cliente if factura.cliente else None

            pdf_buffer = generar_pdf_factura(
                factura,
                cliente,
                DetalleFactura.objects.filter(factura=factura),
            )

            filename = f"{factura.numero_factura}.pdf"
            return FileResponse(pdf_buffer, as_attachment=True, filename=filename)

    # GET (mostrar formulario vacío)
    factura_form = FacturaForm(clientes_qs=clientes_qs)
    producto_form = ProductoEnFacturaForm(productos_qs=productos_qs)

    return render(
        request,
        "factura_form.html",
        {
            "factura_form": factura_form,
            "producto_form": producto_form,
            "productos": productos_qs,
        },
    )


def factura_detalle(request, numero_factura):
    factura = get_object_or_404(
        Factura.objects.select_related("cliente"), numero_factura=numero_factura
    )
    detalles = DetalleFactura.objects.filter(factura=factura)
    return render(
        request,
        "factura_salida.html",
        {"factura": factura, "detalles": detalles},
    )


def reporte_facturas(request):
    facturas = Factura.objects.order_by("-fecha")
    return render(request, "reporte_facturas.html", {"facturas": facturas})


def descargar_factura(request, numero_factura):
    factura = get_object_or_404(
        Factura.objects.select_related("cliente"), numero_factura=numero_factura
    )
    cliente = factura.cliente if factura.cliente else None
    detalles = DetalleFactura.objects.filter(factura=factura)

    pdf = generar_pdf_factura(factura, cliente, detalles)

    return FileResponse(
        pdf, as_attachment=True, filename=f"{factura.numero_factura}.pdf"
    )


def solicitar_fechas_ventas(request):
    return render(request, "solicitar_fechas.html")


# View 2: Procesa las fechas y genera el PDF
def reporte_ventas(request):
    if request.method == "POST":
        # 1. Obtener las fechas del formulario POST
        fecha_inicio_str = request.POST.get("fecha_inicio")
        fecha_fin_str = request.POST.get("fecha_fin")

        try:
            # Convertir strings a objetos date
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
            # Añadir un día a la fecha fin para incluir las ventas de ese día completo
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            # Manejar error si las fechas no son válidas
            return render(request, "error.html", {"mensaje": "Fechas no válidas."})

        # 2. Filtrar las ventas
        ventas_filtradas = Factura.objects.filter(
            fecha__range=[fecha_inicio, fecha_fin]
        ).order_by("fecha")

        # 3. Generar el PDF
        pdf = generar_pdf_ventas(ventas_filtradas, fecha_inicio, fecha_fin)

        filename = f"reporte_ventas_{fecha_inicio_str}_a_{fecha_fin_str}.pdf"

        return FileResponse(pdf, as_attachment=True, filename=filename)

    # Si alguien intenta acceder directamente vía GET, redirigir al formulario
    return redirect("solicitar_fechas_ventas")
