from django.shortcuts import render, redirect
from .forms import FacturaForm


def crear_factura(request):
    if request.method == "POST":
        form = FacturaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crear_factura")
    else:
        form = FacturaForm()

    return render(request, "factura_form.html", {"form": form})
