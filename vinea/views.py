import json
import jsonpickle

from collections import defaultdict
import datetime
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.db import models
from django.shortcuts import render

# Create your views here.
# TODO : s'inspirer des forms du template pour connecter nos propres forms 
# avec notre base de donnée.
from vinea.forms import *
from vinea.models import *

from django.views.generic import ListView, TemplateView
from django.core.serializers.json import DjangoJSONEncoder
from django.views import View


# Form creations
class AddItemsView(CreateView):
    model = Items
    template_name = "vinea/create_item.html"
    form_class = ItemsForm
    success_url = "/items-list"

    def form_invalid(self, form):
        return HttpResponse(form.as_p())


class UpdateItemsView(UpdateView):
    model = Items
    template_name = "vinea/create_item.html"
    form_class = ItemsForm
    success_url = "/items-list"

    def form_invalid(self, form):
        return HttpResponse(form.as_p())

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        item = self.get_object()
        context["supplier_name"] = item.supplier.supplier_name
        context["creating"] = False
        return context

class DeleteViewItems(DeleteView):
    model = Items
    template_name = None
    success_url = reverse_lazy("items-list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class AddOrdersView(CreateView):
    model = Orders
    template_name = "vinea/create_order.html"
    form_class = OrdersForm
    success_url = "/orders-list"

    def form_invalid(self, form):
        return HttpResponse(form.as_p())


class UpdateOrdersView(UpdateView):
    model = Orders
    template_name = "vinea/create_order.html"
    form_class = OrdersForm
    success_url = "/orders-list"

    def form_invalid(self, form):
        return HttpResponse(form.as_p())

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context["item_name"] = order.item.name
        context["supplier_name"] = order.supplier.supplier_name
        context["creating"] = False
        return context

class DeleteViewOrders(DeleteView):
    model = Orders
    template_name = None
    success_url = reverse_lazy("orders_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class AddSalesView(CreateView):
    model = Sales
    template_name = "vinea/create_sales.html"
    form_class = SalesForm
    success_url = "/sales-list"

    def form_invalid(self, form):
        return HttpResponse(form.as_p())


class UpdateSalesView(UpdateView):
    model = Sales
    template_name = "vinea/create_sales.html"
    form_class = SalesForm
    success_url = "/orders-list"

    def form_invalid(self, form):
        return HttpResponse(form.as_p())

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        sale = self.get_object()
        context["item_name"] = sale.item.name
        context["creating"] = False
        return context

class DeleteViewSales(DeleteView):
    model = Sales
    template_name = None
    success_url = reverse_lazy("sales_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class AddSuppliersView(CreateView):
    model = Suppliers
    template_name = "vinea/create_supplier.html"
    form_class = SuppliersForm
    success_url = "/suppliers-list"

    def form_invalid(self, form):
        return HttpResponse(form.as_p())

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["creating"] = True
        return context


class UpdateSuppliersView(UpdateView):
    model = Suppliers
    template_name = "vinea/create_supplier.html"
    form_class = SuppliersForm
    success_url = "/suppliers-list"

    def form_invalid(self, form):
        return HttpResponse(form.as_p())

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["creating"] = False
        return context


class DeleteViewSuppliers(DeleteView):
    model = Suppliers
    template_name = None
    success_url = reverse_lazy("suppliers_list")

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class VineaForm(FormView):
    template_name = "my_html.html"
    form_class = ItemsForm
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def get_suppliers():
    datas = Suppliers.objects.all()
    res = {
        data.supplier_name: data.pk for data in datas
    }
    return res

def api_items_list(request):
    datas = Items.objects.values("name", "pk").distinct()
    res = {
        data["name"].upper(): data["pk"] for data in datas
    }
    return HttpResponse(json.dumps(res), content_type='application/json')

def api_items_forecast(request):
    datas = Items.objects.values("name","volume", "pk").distinct()
    res = {
        data["name"].upper(): {"pk" :  data["pk"], "volume" :  data["volume"]} for data in datas
    }
    return HttpResponse(json.dumps(res), content_type='application/json')

def api_timeline_data(request):
    item_id = request.GET.get("item_id")
    timeline_data = Forecasts.objects.filter(item__id=item_id).order_by("month").values("month","forecasted","actual")
    res = {
        "actual" : [row['actual'] for row in timeline_data],
        "forecast" : [row['forecasted'] for row in timeline_data],
        "months" : [row['month'] for row in timeline_data]
    }
    return HttpResponse(json.dumps(res), content_type='application/json')


def api_supplier_list(request):
    res = get_suppliers()
    return HttpResponse(json.dumps(res), content_type='application/json')


def VineaFormView(request):
    form = VineaFormEntries()
    return render(request=request, template_name="my_html.html", context={
        "form": form
    })


def api_get_order_by_page(request):
    order_list = Orders.objects.all()
    paginator = Paginator(order_list, 50)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    data = map(lambda order: {"order_date": order.order_date.strftime("%b .%d, %Y"),
                              "order_number": order.order_number,
                              "reception_date": order.reception_date.strftime("%b .%d, %Y"),
                              "purchase_price": order.purchase_price,
                              "quantity": order.quantity,
                              "total_price": order.total_price,
                              "item": order.item.name,
                              "supplier": order.supplier.supplier_name,
                              "pk": order.pk
                              }, page_obj)
    data = list(data)
    return HttpResponse(json.dumps(data), content_type="application/json")


def api_get_items_by_page(request):
    items_list = Items.objects.all()
    paginator = Paginator(items_list, 50)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    data = map(lambda item: {"name": item.name,
                             "volume": item.volume,
                             "sale_price": item.sale_price,
                             "on_hand": item.on_hand,
                             "supplier": item.supplier.supplier_name,
                             "group": item.group,
                             "pk": item.pk
                             }, page_obj)
    data = list(data)
    return HttpResponse(json.dumps(data), content_type="application/json")


def api_get_suppliers_by_page(request):
    suppliers_list = Suppliers.objects.all()
    paginator = Paginator(suppliers_list, 50)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    data = map(lambda supplier: {"supplier_name": supplier.supplier_name,
                                 "contact": supplier.contact,
                                 "address": supplier.address,
                                 "email": supplier.email,
                                 "pk": supplier.pk
                                 }, page_obj)
    data = list(data)
    return HttpResponse(json.dumps(data), content_type="application/json")


def api_get_sales_by_page(request):
    sales_list = Sales.objects.all()
    paginator = Paginator(sales_list, 50)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    data = map(lambda sale: {"quantity": sale.quantity,
                             "unit_price": sale.unit_price,
                             "date": sale.date.strftime("%b .%d, %Y"),
                             "item": sale.item.name,
                             "pk": sale.pk
                             }, page_obj)
    data = list(data)
    return HttpResponse(json.dumps(data), content_type="application/json")


class OrderListView(ListView):
    template_name = "dashboard.html"
    ordering = "id"
    paginate_by = 50
    model = Orders
    sales_df = Sales.objects.all().to_dataframe()

    # https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-display/
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        total_product = Items.objects.count()
        total_supplier = Suppliers.objects.count()
        total_sales = int((self.sales_df['quantity'] * self.sales_df['unit_price']).sum())
        total_order = Orders.objects.count()
        # Add in a QuerySet of all the books
        # print("context",context)
        context["page_obj"].adjusted_elided_pages = context["paginator"].get_elided_page_range(
            context["page_obj"].number)
        context.update({
            "paginate_by": self.paginate_by,
            "page_index": context["page_obj"].number - 1,
            'product': total_product,
            'supplier': total_supplier,
            'revenue': total_sales,
            'order': total_order,
            "url_name": "dashboard"
        })
        return context


class ItemsListView(ListView):
    template_name = "vinea/items_list.html"
    ordering = "id"
    paginate_by = 50
    model = Items

    # https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-display/
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["page_obj"].adjusted_elided_pages = context["paginator"].get_elided_page_range(
            context["page_obj"].number)
        context.update({
            "paginate_by": self.paginate_by,
            "page_index": context["page_obj"].number - 1,
            "url_name": "items_list"
        })
        return context


class OrdersListView(ListView):
    template_name = "vinea/order_list.html"
    ordering = "id"
    paginate_by = 50
    model = Orders

    # https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-display/
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["page_obj"].adjusted_elided_pages = context["paginator"].get_elided_page_range(
            context["page_obj"].number)
        context.update({
            "paginate_by": self.paginate_by,
            "page_index": context["page_obj"].number - 1,
            "url_name": "orders_list"
        })
        return context


class SuppliersListView(ListView):
    template_name = "vinea/supplier_list.html"
    ordering = "id"
    paginate_by = 50
    model = Suppliers

    # https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-display/
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["page_obj"].adjusted_elided_pages = context["paginator"].get_elided_page_range(
            context["page_obj"].number)
        context.update({
            "paginate_by": self.paginate_by,
            "page_index": context["page_obj"].number - 1,
            "url_name": "suppliers_list"
        })
        return context


class SalesListView(ListView):
    template_name = "vinea/sale_list.html"
    ordering = "id"
    paginate_by = 50
    model = Sales

    # https://docs.djangoproject.com/en/4.2/topics/class-based-views/generic-display/
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["page_obj"].adjusted_elided_pages = context["paginator"].get_elided_page_range(
            context["page_obj"].number)
        context.update({
            "paginate_by": self.paginate_by,
            "page_index": context["page_obj"].number - 1,
            "url_name": "sales_list"
        })
        return context


class InventoryCheckView(TemplateView):
    # Check_inventory view
    # Génération par la système des recommandations d'approvisionnement

    template_name = 'vinea/check_inventory.html'

    def get_context_data(self, **kwargs):
        # Filter items below the threshold
        threshold = 6  # Threshold
        low_inventory_items = Items.objects.filter(on_hand__lte=models.F('order_point')).select_related('supplier')
        last_order_number = {
            'last_order_number': Orders.objects.aggregate(models.Max('order_number'))['order_number__max']}

        # Serialize QuerySet to JSON
        low_inventory_items_json = [dic["fields"] for dic in json.loads(serialize('json', low_inventory_items))]

        grouped_items = defaultdict(list)

        for dic in low_inventory_items_json:
            dic["name"] = dic["name"].replace("'", "_")  # Replacing the single quotes to avoid errors on pdf generation

            # Fetch supplier name using the 'supplier_id' in the dictionary
            supplier_id = dic.get('supplier')
            if supplier_id is not None:
                try:
                    supplier = Suppliers.objects.get(pk=supplier_id)
                    dic['supplier'] = supplier.supplier_name
                except Suppliers.DoesNotExist:
                    dic['supplier'] = f"Unknown Supplier (ID: {supplier_id})"

            grouped_items[dic["supplier"]].append({key: value for key, value in dic.items() if key != "supplier" and key!="on_hand"})

        # Convert the defaultdict to a list of dictionaries
        grouped_items_list = [{'Supplier_name': key, 'items': value} for key, value in grouped_items.items()]

        # Add the items and threshold to the context
        context = super().get_context_data(**kwargs)
        context['last_order_number_json'] = last_order_number
        context['low_inventory_items'] = low_inventory_items
        context['low_inventory_items_json'] = low_inventory_items_json
        context['grouped_items_list_json'] = grouped_items_list
        context['threshold'] = threshold
        context['count'] = low_inventory_items.count()
        return context

class ForecastView(CreateView):
    model = Forecasts
    template_name = "vinea/forecast.html"
    form_class = ForecastForm
    success_url = "/forecast"

@csrf_exempt
def api_add_orders(request):
    data = json.loads(request.body)
    order = Orders(
        order_number = data['order_number'],
        order_date = datetime.datetime.today(),
        reception_date = datetime.datetime(1999,1,1).date(),
        purchase_price = data['purchase_price'],
        quantity = data['quantity'],
        total_price = data['total_price'],
        item = Items.objects.get(name = data['item']),
        supplier = Suppliers.objects.get(supplier_name = data['supplier'])
    )
    order.save()

    return HttpResponse("successful", content_type="application/json")

