from django.shortcuts import render, redirect
from .forms import ClienteForm


def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crear_cliente")
    else:
        form = ClienteForm()

    return render(request, "cliente_form.html", {"form": form})
