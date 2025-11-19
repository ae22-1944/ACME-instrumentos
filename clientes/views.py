from django.shortcuts import render, redirect
from .forms import ClienteForm
from .models import Cliente


def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crear_cliente")
    else:
        form = ClienteForm()

    return render(request, "cliente_form.html", {"form": form})


def reporte_clientes(request):
    clientes = Cliente.objects.order_by("nombre")
    return render(request, "reporte_clientes.html", {"clientes": clientes})


def menu_clientes(request):
    return render(request, "clientes_menu.html")
