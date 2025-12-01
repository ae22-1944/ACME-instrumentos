from django.urls import path
from .views import (
    crear_editar_producto,
    borrar_producto,
    crear_categoria,
    borrar_categoria,
    menu_inventario,
    reporte_inventario,
)

urlpatterns = [
    path("", menu_inventario, name="inventario"),
    path("producto/nuevo/", crear_editar_producto, name="crear_producto"),
    path("<int:pk>/borrar/", borrar_producto, name="borrar_producto"),
    path("productos/<str:codigo>", crear_editar_producto, name="producto_detalle"),
    path("categoria/nueva/", crear_categoria, name="crear_categoria"),
    path("categorias/<int:pk>/borrar/", borrar_categoria, name="borrar_categoria"),
    path("reporte/", reporte_inventario, name="reporte_inventario"),
]
