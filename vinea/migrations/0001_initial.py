# Generated by Django 3.2.23 on 2024-01-11 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('volume', models.FloatField()),
                ('sale_price', models.FloatField()),
                ('purchase_price', models.FloatField()),
                ('on_hand', models.IntegerField()),
                ('group', models.CharField(default='A', max_length=120)),
                ('order_quantity', models.IntegerField(default=1)),
                ('order_point', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.CreateModel(
            name='Suppliers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_name', models.CharField(max_length=120, unique=True)),
                ('contact', models.CharField(max_length=120, unique=True)),
                ('address', models.CharField(max_length=120, unique=True)),
                ('email', models.CharField(max_length=120, unique=True)),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('date', models.DateField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vinea.items')),
            ],
            options={
                'verbose_name': 'Sale',
                'verbose_name_plural': 'Sales',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField()),
                ('order_date', models.DateField()),
                ('reception_date', models.DateField()),
                ('purchase_price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('total_price', models.FloatField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vinea.items')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vinea.suppliers')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.AddField(
            model_name='items',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vinea.suppliers'),
        ),
    ]