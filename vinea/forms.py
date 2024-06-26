from django import forms
from vinea.models import Items, Suppliers, Orders, Sales, Forecasts
from django.core.exceptions import ValidationError

ITEMS_GROUPS = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
)


class SuppliersForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields = ['supplier_name', 'contact', "address", "email"]
        widgets = {
            'supplier_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'supplier_name'
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'phone'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'address'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'email'
            }),
        }


class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['quantity', 'unit_price', "date", "item"]
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control', 'id': 'date', "type": "date"
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'quantity', "value": 1
            }),
            'unit_price': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'unit_price',"value":0
            }),
            'item': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'item'
            }),
        }

class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = ['name', 'volume', "sale_price", "on_hand", "purchase_price", "group", "supplier"]
        widgets = {
            'supplier': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'supplier'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name'
            }),
            'volume': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'volume', "value": 0
            }),
            'sale_price': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'sale_price', "value": 0
            }),
            'on_hand': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'on_hand', "value": 0
            }),
            'purchase_price': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'purchase_price', "value": 0
            }),
            'group': forms.Select(attrs={
                'class': 'form-control', 'id': 'group'
            }, choices=ITEMS_GROUPS)
        }


class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['order_number', 'order_date', "reception_date", "purchase_price", "quantity", "total_price", "item",
                  "supplier"]
        widgets = {
            'supplier': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'supplier'
            }),
            'item': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'item'
            }),
            'order_date': forms.DateInput(attrs={
                'class': 'form-control', 'id': 'order_date', "type": "date"
            }),
            'reception_date': forms.DateInput(attrs={
                'class': 'form-control', 'id': 'reception_date', "type": "date"
            }),
            'order_number': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'order_number', "value": 0
            }),
            'purchase_price': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'purchase_price', "value": 0
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'quantity', "value": 0
            }),
            'total_price': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'total_price', "value": 0
            }),

        }


class VineaFormEntries(forms.ModelForm):
    # team_name = forms.CharField(required=True,help_text="this is a demo")
    class Meta:
        model = Items
        fields = ["name", "volume", "sale_price", "purchase_price"]
        help_texts = {
            "name": "Please enter a name",
            "volume": "Please enter a volume",
            "sale_price": "Please enter a saleprice"
        }

    def clean_name(self):
        data = self.cleaned_data["name"]
        if not data.startswith("FC"):
            raise ValidationError(f'{data} need to start with FC')
        return data

class ForecastForm(forms.ModelForm):
    # Use ModelChoiceField as the form field for the 'name' field
    # name = forms.ModelChoiceField(queryset=Items.objects.all(), empty_label="Select an item")

    class Meta:
        model = Forecasts
        fields = ['item']
        widgets = {
           'item': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'item'
            })

        }

