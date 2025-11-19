from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm, CategoriaForm


def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crear_producto")
    else:
        form = ProductoForm()

    return render(request, "producto_form.html", {"form": form})


def crear_categoria(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crear_categoria")
    else:
        form = CategoriaForm()

    return render(request, "categoria_form.html", {"form": form})


def reporte_inventario(request):
    productos = Producto.objects.order_by("nombre")
    return render(request, "reporte_inventario.html", {"productos": productos})


def menu_inventario(request):
    return render(request, "inventario_menu.html")
