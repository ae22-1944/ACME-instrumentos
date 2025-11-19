from django.urls import path
from .views import crear_producto, crear_categoria, reporte_inventario, menu_inventario

urlpatterns = [
    path("", menu_inventario, name="menu_inventario"),
    path("producto/nuevo/", crear_producto, name="crear_producto"),
    path("categoria/nueva/", crear_categoria, name="crear_categoria"),
    path("reporte/", reporte_inventario, name="reporte_inventario"),
]
