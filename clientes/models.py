from django.db import models


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    rnc_cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100, unique=True)
    STATUS_CHOICES = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]
    estado = models.CharField(max_length=10, choices=STATUS_CHOICES, default="activo")

    def __str__(self):
        return self.nombre
