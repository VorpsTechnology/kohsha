# Generated by Django 4.2.1 on 2023-05-26 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_order_weight_products_height_products_width'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='product_qty',
            field=models.IntegerField(null=True),
        ),
    ]