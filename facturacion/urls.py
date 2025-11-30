from django.urls import path
from .views import (
    crear_factura,
    descargar_factura,
    factura_detalle,
    reporte_facturas,
    reporte_ventas,
    solicitar_fechas_ventas,
)

urlpatterns = [
    path("nuevo/", crear_factura, name="crear_factura"),
    path("ventas/", reporte_facturas, name="ventas"),
    path("<str:numero_factura>/", factura_detalle, name="factura_detalle"),
    path(
        "<str:numero_factura>/descargar/", descargar_factura, name="descargar_factura"
    ),
    path("reporte/ventas/", reporte_ventas, name="reporte_ventas"),
    path(
        "reporte/ventas/solicitar/",
        solicitar_fechas_ventas,
        name="solicitar_fechas_ventas",
    ),
]
