from django.db import models
from django.utils.text import slugify
from django.db.models import Max


class CategoriaProducto(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.descripcion


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10, unique=True, blank=True, editable=False)
    nombre = models.CharField(max_length=50, unique=True)
    imagen = models.ImageField(upload_to="productos/", null=True, blank=True)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(
        "proveedores.Proveedor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos",
    )
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField()
    stock_minimo = models.IntegerField()
    creado_en = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk or not self.codigo:
            cat_slug = slugify(self.categoria.descripcion).replace("-", "").upper()[:6]

            prefix = f"{cat_slug[:3]}-"

            last_product = Producto.objects.filter(codigo__startswith=prefix).aggregate(
                Max("codigo")
            )

            new_sequence = 1
            if last_product["codigo__max"]:
                try:
                    current_number = int(last_product["codigo__max"].split("-")[-1])
                    new_sequence = current_number + 1
                except ValueError:
                    pass

            self.codigo = f"{prefix}{new_sequence:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
