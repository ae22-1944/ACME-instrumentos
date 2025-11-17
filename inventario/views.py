from django.shortcuts import render, redirect
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
