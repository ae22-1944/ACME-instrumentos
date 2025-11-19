from django.urls import path
from .views import crear_cliente, reporte_clientes, menu_clientes

urlpatterns = [
    path("", menu_clientes, name="menu_clientes"),
    path("nuevo/", crear_cliente, name="crear_cliente"),
    path("reporte/", reporte_clientes, name="reporte_clientes"),
]
