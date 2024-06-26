from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import *


from store.models import Product, Supplier, Buyer, Order
from vinea.models import *


@login_required(login_url='login')
def dashboard(request):
    total_product = Items.objects.count()
    total_supplier = Suppliers.objects.count()
    total_sales = int(sum(sales.quantity * sales.unit_price for sales in Sales.objects.all())) #F est utilisé pour référencer une ligne
    total_order = Orders.objects.count()
    # orders = Order.objects.all().order_by('-id')
    orders = Orders.objects.all().order_by('-id')[:10]
    context = {
        'product': total_product,
        'supplier': total_supplier,
        'revenue': total_sales,
        'order': total_order,
        'orders': orders
    }
    return render(request, 'dashboard.html', context)
