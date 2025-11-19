from django.contrib import admin
from django.urls import path, include
from .views import home


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("clientes/", include("clientes.urls")),
    path("proveedores/", include("proveedores.urls")),
    path("inventario/", include("inventario.urls")),
    path("facturacion/", include("facturacion.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
