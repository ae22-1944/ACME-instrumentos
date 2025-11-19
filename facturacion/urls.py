from django.urls import path
from .views import (
    crear_factura,
    factura_detalle,
    reporte_facturas,
    reporte_ventas,
    menu_facturacion,
)

urlpatterns = [
    path("", menu_facturacion, name="menu_facturacion"),
    path("nuevo/", crear_factura, name="crear_factura"),
    path("reporte/", reporte_facturas, name="reporte_facturas"),
    path("ventas/", reporte_ventas, name="reporte_ventas"),
    path("<str:numero_factura>/", factura_detalle, name="factura_salida"),
]
