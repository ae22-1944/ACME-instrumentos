from django.urls import path
from .views import crear_producto, crear_categoria

urlpatterns = [
    path("producto/nuevo/", crear_producto, name="crear_producto"),
    path("categoria/nueva/", crear_categoria, name="crear_categoria"),
]
