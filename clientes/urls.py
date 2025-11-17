from django.urls import path
from .views import crear_cliente

urlpatterns = [
    path("nuevo/", crear_cliente, name="crear_cliente"),
]
