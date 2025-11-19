from django.shortcuts import render, redirect
from .forms import ProveedorForm
from .models import Proveedor


def crear_proveedor(request):
    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crear_proveedor")
    else:
        form = ProveedorForm()

    return render(request, "proveedor_form.html", {"form": form})


def reporte_proveedores(request):
    proveedores = Proveedor.objects.order_by("nombre")
    return render(request, "reporte_proveedores.html", {"proveedores": proveedores})


def menu_proveedores(request):
    return render(request, "proveedores_menu.html")
