from django.urls import path
from .views import (
    crear_editar_proveedor,
    borrar_proveedor,
    menu_proveedores,
    reporte_proveedores,
)

urlpatterns = [
    path("", menu_proveedores, name="proveedores"),
    path("reporte/", reporte_proveedores, name="reporte_proveedores"),
    path("nuevo/", crear_editar_proveedor, name="crear_proveedor"),
    path("<int:pk>", crear_editar_proveedor, name="proveedor_detalle"),
    path("<int:pk>/borrar/", borrar_proveedor, name="borrar_proveedor"),
]
