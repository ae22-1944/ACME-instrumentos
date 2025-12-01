from django.shortcuts import render
from django.db.models import Sum
from inventario.models import Producto
from clientes.models import Cliente
from proveedores.models import Proveedor
from facturacion.models import Factura
from datetime import datetime


def home(request):
    context = {}
    
    # Solo agregar estadísticas si es administrador
    if request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name="Administrador").exists()):
        # Contar productos
        total_productos = Producto.objects.count()
        
        # Contar clientes
        total_clientes = Cliente.objects.count()
        
        # Contar proveedores
        total_proveedores = Proveedor.objects.count()
        
        # Sumar ventas del día - CORREGIDO: usar datetime.now().date() en vez de date.today()
        hoy = datetime.now().date()
        ventas_hoy = Factura.objects.filter(fecha__date=hoy).aggregate(
            total=Sum('total')
        )['total'] or 0
        
        context['estadisticas'] = {
            'productos': total_productos,
            'clientes': total_clientes,
            'proveedores': total_proveedores,
            'ventas_hoy': ventas_hoy,
            'es_admin': True
        }
    else:
        context['estadisticas'] = {'es_admin': False}
    
    return render(request, "home.html", context)