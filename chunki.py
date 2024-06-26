import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory.settings')
django.setup()

from vinea.models import Suppliers,Items,Sales,Orders, Forecasts

from django.db.models import Sum, Avg

import random

# suppliers = pd.read_csv("data_corrected/suppliers.csv",)

# for i,row in suppliers.iterrows():
#     supplier = Suppliers(supplier_name = row["Supplier Name"], contact = row["Contact"], address=row["Address"] , email = row["Email"])
#     supplier.save()

# items = pd.read_csv("data_corrected/items.csv",)

# for i,row in items.iterrows():
#         item = Items(name = row["Name"], \
#                     volume = row["Volume"], \
#                         sale_price=row["Sale price"] , \
#                             purchase_price = row["Purchase price"],\
#                                 on_hand = row["OnHand"],\
#                                     supplier = Suppliers.objects.get(id=row['id supplier']))
#         item.save()

# sales = pd.read_csv("data_corrected/sales.csv",)

# for i,row in sales.iterrows():
#         sale = Sales(date = row["Date"], \
#                      quantity = row["Quantity"],\
#                      unit_price = row["Unit price"],\
#                     item = Items.objects.get(id=row['id item']))
#         sale.save()

#Order Date,Receiving Date,Purchase price,Quantity,Total price,Order number,id item,id supplier

# orders = pd.read_csv("data_corrected/orders.csv",)

# for i,row in orders.iterrows():
#         print(f"{i+1}/1257 done!")
#         order = Orders(order_number = row["Order number"],
#                      order_date = row["Order Date"],
#                      reception_date = row["Receiving Date"],
#                      purchase_price = row["Purchase price"],
#                      quantity = row["Quantity"],
#                      total_price = row["Total price"],
#                     item = Items.objects.get(id=row['id item']),
#                     supplier = Suppliers.objects.get(id=row['id supplier']))
#         order.save()

# for ind, item in enumerate(Items.objects.all()):

#         sales = Sales.objects.filter(item__name=item.name)

#         monthly_sales = (
#         sales
#         .values('date__year', 'date__month')
#         .annotate(actual=Sum('quantity'))
#         )

#         for index,record in enumerate(monthly_sales):
#                 if index < len(monthly_sales)-1:
#                         forecast = Forecasts(
#                                 year = record['date__year'],
#                                 month = record['date__month'],
#                                 item = item,
#                                 forecasted = (monthly_sales[index]["actual"]+monthly_sales[index+1]["actual"])//2,
#                                 actual = record['actual']
#                         )
#                 else:
#                         forecast = Forecasts(
#                                 year = record['date__year'],
#                                 month = record['date__month'],
#                                 item = item,
#                                 forecasted = (monthly_sales[index]["actual"]+monthly_sales[0]["actual"])//2,
#                                 actual = record['actual']
#                         )

#                 forecast.save()

#         print(f'{ind*100/len(Items.objects.all())} %')

timeline_data = Forecasts.objects.filter(item__id=1).order_by("month").values("forecasted","actual")

print(timeline_data)

# Parcourir le record de tous les items
### Pour chaque item
######determiner le monthly sales
######Ajouter le resultat dans la table forecast
