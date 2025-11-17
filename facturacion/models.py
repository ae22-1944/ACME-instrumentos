from django.db import models


class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    numero_factura = models.CharField(max_length=20)
    fecha = models.DateTimeField()
    cliente = models.ForeignKey("clientes.Cliente", on_delete=models.CASCADE)
    metodo_pago = models.CharField(max_length=20)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    itbis = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.numero_factura


class DetalleFactura(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey("inventario.Producto", on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id_detalle} - {self.factura.numero_factura}"
