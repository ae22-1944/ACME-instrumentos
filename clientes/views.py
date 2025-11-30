from django.shortcuts import get_object_or_404, render, redirect
from django.http import FileResponse
from .forms import ClienteForm
from .models import Cliente
from reportes.clientes_pdf import generar_pdf_clientes


def menu_clientes(request):
    clientes = Cliente.objects.order_by("nombre")
    return render(request, "clientes_menu.html", {"clientes": clientes})


def crear_editar_cliente(request, pk=None):
    cliente = get_object_or_404(Cliente, pk=pk) if pk is not None else None

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("clientes")
    else:
        form = ClienteForm(instance=cliente)

    return render(
        request,
        "cliente_form.html",
        {
            "form": form,
            "editando": cliente is not None,
        },
    )


def borrar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect("clientes")


def reporte_clientes(request):
    clientes = Cliente.objects.all().order_by("nombre")
    pdf = generar_pdf_clientes(clientes)
    return FileResponse(pdf, as_attachment=True, filename="reporte_clientes.pdf")
