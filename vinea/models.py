from django.db import models
from django_pandas.managers import DataFrameManager

# Create your models here.
# the following classes
# https://www.geeksforgeeks.org/python-relational-fields-in-django-models/

class Items(models.Model):
    name = models.CharField(max_length=120)
    volume = models.FloatField()
    sale_price = models.FloatField()  # Is this a repetition ?
    purchase_price = models.FloatField()
    on_hand = models.IntegerField()  # Same here ?
    group = models.CharField(max_length=120, default='A')
    order_quantity = models.IntegerField(default=1)
    order_point = models.IntegerField(default=0)
    # relation with supplier
    supplier = models.ForeignKey("Suppliers", on_delete=models.CASCADE)

    objects = DataFrameManager()
    
    class Meta:
        verbose_name = "Item"  # Singular form
        verbose_name_plural = "Items"  # Plural form

    def __str__(self):
        return self.name


class Orders(models.Model):
    order_number = models.IntegerField()
    order_date = models.DateField()
    reception_date = models.DateField()
    purchase_price = models.FloatField()
    quantity = models.IntegerField()
    total_price = models.FloatField()
    # id_item et id_supplier
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    supplier = models.ForeignKey("Suppliers", on_delete=models.CASCADE) # Supplier is in quotes because it not yet defined

    objects = DataFrameManager()

    def __str__(self):
        return f"Order number {str(self.order_number)}"

    class Meta:
        verbose_name = "Order"  # Singular form
        verbose_name_plural = "Orders"  # Plural form


class Suppliers(models.Model):
    supplier_name = models.CharField(max_length=120, unique=True)
    contact  = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=120, unique=True)
    email = models.CharField(max_length=120,unique=True)

    objects = DataFrameManager()

    def __str__(self):
        return self.supplier_name
    class Meta:
        verbose_name = "Supplier"  # Singular form
        verbose_name_plural = "Suppliers"  # Plural form



class Sales(models.Model):
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    date = models.DateField()
    # relation with items
    item = models.ForeignKey(Items, on_delete=models.CASCADE)

    objects = DataFrameManager()

    def __str__(self) -> str:
        return self.date.strftime("%d/%m/%y")

    class Meta:
        verbose_name = "Sale"  # Singular form
        verbose_name_plural = "Sales"  # Plural form

class Forecasts(models.Model):
    
    year = models.IntegerField()
    month = models.IntegerField()
    item = models.ForeignKey("Items", on_delete=models.CASCADE)
    forecasted = models.IntegerField()
    actual = models.IntegerField()

    objects = DataFrameManager()

    def __str__(self):
        return self.supplier_name
    class Meta:
        verbose_name = "Forecast"  # Singular form
        verbose_name_plural = "Forecasts"  # Plural form
