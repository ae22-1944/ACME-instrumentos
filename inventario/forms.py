from django import forms
from .models import Producto, CategoriaProducto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = "__all__"
