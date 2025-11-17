from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("clientes/", include("clientes.urls")),
    path("proveedores/", include("proveedores.urls")),
    path("inventario/", include("inventario.urls")),
    path("facturacion/", include("facturacion.urls")),
]
