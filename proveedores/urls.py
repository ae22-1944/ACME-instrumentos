from django.urls import path
from .views import crear_proveedor, reporte_proveedores, menu_proveedores

urlpatterns = [
    path("", menu_proveedores, name="menu_proveedores"),
    path("nuevo/", crear_proveedor, name="crear_proveedor"),
    path("reporte/", reporte_proveedores, name="reporte_proveedores"),
]
