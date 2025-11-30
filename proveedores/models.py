from django.db import models


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    categorias = models.ManyToManyField(
        "inventario.CategoriaProducto", related_name="proveedores", blank=True
    )
    direccion = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    rnc_cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(max_length=100)
    STATUS_CHOICES = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]
    estado = models.CharField(max_length=10, choices=STATUS_CHOICES, default="activo")

    def __str__(self):
        return self.nombre
