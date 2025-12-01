from django import forms
from .models import Proveedor
from inventario.models import CategoriaProducto


class ProveedorForm(forms.ModelForm):
    categorias = forms.ModelMultipleChoiceField(
        queryset=CategoriaProducto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,  # Ahora es obligatorio
        label="Categorías",
        help_text="Seleccione al menos una categoría"
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

    def clean_categorias(self):
        categorias = self.cleaned_data.get('categorias')
        if not categorias or categorias.count() == 0:
            raise forms.ValidationError("Debe seleccionar al menos una categoría")
        return categorias