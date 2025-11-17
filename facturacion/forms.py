from django import forms
from .models import Factura, DetalleFactura


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = "__all__"


class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = "__all__"
