from django.db import models


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    rnc_cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=15)
    contacto = models.CharField(max_length=40)
    correo = models.CharField(max_length=100)
    estado = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre


class ProveedorProducto(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    producto = models.ForeignKey("inventario.Producto", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("proveedor", "producto")

    def __str__(self):
        return f"{self.proveedor.nombre} - {self.producto.nombre}"
