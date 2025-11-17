from django.urls import path
from .views import crear_proveedor

urlpatterns = [
    path("nuevo/", crear_proveedor, name="crear_proveedor"),
]
