from django import forms
from .models import Proveedor
from inventario.models import CategoriaProducto


class ProveedorForm(forms.ModelForm):

    categorias = forms.ModelMultipleChoiceField(
        queryset=CategoriaProducto.objects.all(),
        widget=forms.SelectMultiple,
        required=False,
    )

    class Meta:
        model = Proveedor
        fields = [
            "nombre",
            "categorias",
            "direccion",
            "rnc_cedula",
            "telefono",
            "contacto",
            "correo",
            "estado",
        ]
