from django.urls import path
from .views import crear_editar_cliente, borrar_cliente, menu_clientes, reporte_clientes

urlpatterns = [
    path("", menu_clientes, name="clientes"),
    path("nuevo/", crear_editar_cliente, name="crear_cliente"),
    path("<int:pk>", crear_editar_cliente, name="cliente_detalle"),
    path("<int:pk>/borrar/", borrar_cliente, name="borrar_cliente"),
    path("reporte/", reporte_clientes, name="reporte_clientes"),
]
