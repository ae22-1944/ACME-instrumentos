from django import forms
from .models import Factura
from inventario.models import Producto


class FacturaForm(forms.ModelForm):
    METODOS = [
        ("efectivo", "Efectivo"),
        ("tarjeta", "Tarjeta de crédito/débito"),
        ("transferencia", "Transferencia"),
    ]

    metodo_pago = forms.ChoiceField(choices=METODOS, label="Método de pago")

    class Meta:
        model = Factura
        fields = ["cliente", "metodo_pago"]

    def __init__(self, *args, **kwargs):
        clientes_qs = kwargs.pop("clientes_qs", None)
        super().__init__(*args, **kwargs)
        if clientes_qs is not None:
            self.fields["cliente"].queryset = clientes_qs


class ProductoEnFacturaForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=None, label="Producto")
    cantidad = forms.IntegerField(min_value=1, label="Cantidad")

    def __init__(self, *args, **kwargs):
        productos_qs = kwargs.pop("productos_qs", None)
        super().__init__(*args, **kwargs)
        if productos_qs is not None:
            self.fields["producto"].queryset = productos_qs
