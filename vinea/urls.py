from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    # ex: /
    path("", login_required(views.OrderListView.as_view(), login_url="login"), name="dashboard"),
    path("create-items/",views.AddItemsView.as_view(),name="create-item"),
    path("create-oders/",views.AddOrdersView.as_view(),name="create-orders"),
    path("create-suppliers/",views.AddSuppliersView.as_view(),name="create-suppliers"),
    path("create-sales/",views.AddSalesView.as_view(),name="create-sales"),
    path("thabel/", views.VineaForm.as_view(), name="thabel"),
    path("api-suppliers",views.api_supplier_list,name="api_supplier"),
    path('inventory-check/', views.InventoryCheckView.as_view(), name='inventory-check'),
    path('forecast/', views.ForecastView.as_view(), name='forecast'),
    path("items-list/", views.ItemsListView.as_view(), name="items_list"),
    path("orders-list/", views.OrdersListView.as_view(), name="orders_list"),
    path("suppliers-list/", views.SuppliersListView.as_view(), name="suppliers_list"),
    path("sales-list/", views.SalesListView.as_view(), name="sales_list"),
    path("sales-list/", views.SalesListView.as_view(), name="sales_list"),

    # Updates views
    path("update-suppliers/<int:pk>", views.UpdateSuppliersView.as_view(), name="update-suppliers"),
    path("update-sales/<int:pk>", views.UpdateSalesView.as_view(), name="update-sales"),
    path("update-orders/<int:pk>", views.UpdateOrdersView.as_view(), name="update-orders"),
    path("update-items/<int:pk>", views.UpdateItemsView.as_view(), name="update-items"),
    # Delete Views
    path("delete-suppliers/<int:pk>",views.DeleteViewSuppliers.as_view(),name="delete_suppliers"),
    path("delete-sales/<int:pk>", views.DeleteViewSales.as_view(), name="delete_sales"),
    path("delete-orders/<int:pk>", views.DeleteViewOrders.as_view(), name="delete_orders"),
    path("delete-items/<int:pk>", views.DeleteViewItems.as_view(), name="delete_items"),

    path("api_get_order_by_page",views.api_get_order_by_page,name="api_get_order_by_page"),
    path("api_get_items_by_page", views.api_get_items_by_page, name="api_get_items_by_page"),
    path("api_get_suppliers_by_page", views.api_get_suppliers_by_page, name="api_get_suppliers_by_page"),
    path("api_get_sales_by_page", views.api_get_sales_by_page, name="api_get_sales_by_page"),
    path("api_items_list",views.api_items_list,name="api_items_list"),
    path("api_items_forecast",views.api_items_forecast,name="api_items_forecast"),
    path("api_timeline_data",views.api_timeline_data,name="api_timeline_data"),
    path("api_add_orders",views.api_add_orders,name="api_add_orders")
    # path("thabel/", views.VineaFormView, name="thabel"),
]
