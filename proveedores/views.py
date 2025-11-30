from django.http import FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ProveedorForm
from .models import Proveedor
from reportes.proveedores_pdf import generar_pdf_proveedores


def menu_proveedores(request):
    proveedores = Proveedor.objects.prefetch_related("categorias").order_by("nombre")
    return render(request, "proveedores_menu.html", {"proveedores": proveedores})


def crear_editar_proveedor(request, pk=None):
    proveedor = get_object_or_404(Proveedor, pk=pk) if pk is not None else None

    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect("proveedores")
    else:
        form = ProveedorForm(instance=proveedor)

    return render(
        request,
        "proveedor_form.html",
        {
            "form": form,
            "editando": proveedor is not None,
        },
    )


def editar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return render(
        request,
        "proveedor_form.html",
        {"form": ProveedorForm(instance=proveedor)},
    )


def borrar_proveedor(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    proveedor.delete()
    return redirect("proveedores")


def reporte_proveedores(request):
    proveedores = Proveedor.objects.all().order_by("nombre")
    pdf = generar_pdf_proveedores(proveedores)
    return FileResponse(pdf, as_attachment=True, filename="reporte_proveedores.pdf")
