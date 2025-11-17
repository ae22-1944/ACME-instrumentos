from django.urls import path
from .views import crear_factura

urlpatterns = [
    path("nuevo/", crear_factura, name="crear_factura"),
]
