from django.http import FileResponse
from django.shortcuts import get_object_or_404, render, redirect

from reportes.inventario_pdf import generar_pdf_inventario
from .models import Producto, CategoriaProducto
from .forms import ProductoForm, CategoriaForm


def crear_editar_producto(request, codigo=None):
    producto = (
        get_object_or_404(Producto, codigo=codigo) if codigo is not None else None
    )

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("inventario" if producto else "crear_producto")
    else:
        form = ProductoForm(instance=producto)

    return render(
        request, "producto_form.html", {"form": form, "editando": producto is not None}
    )


def crear_categoria(request):
    categorias = CategoriaProducto.objects.order_by("descripcion")

    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crear_categoria")
    else:
        form = CategoriaForm()

    return render(
        request, "categoria_form.html", {"form": form, "categorias": categorias}
    )


def borrar_categoria(request, pk):
    categoria = get_object_or_404(CategoriaProducto, pk=pk)
    categoria.delete()
    return redirect("crear_categoria")


def menu_inventario(request):
    productos = Producto.objects.select_related("proveedor", "categoria").order_by(
        "nombre"
    )
    return render(request, "inventario_menu.html", {"productos": productos})


def reporte_inventario(request):
    inventario = Producto.objects.all().order_by("nombre")
    pdf = generar_pdf_inventario(inventario)
    return FileResponse(pdf, as_attachment=True, filename="reporte_inventario.pdf")
