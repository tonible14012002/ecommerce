# Generated by Django 4.0.4 on 2022-06-12 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_product_stock_images'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Images',
            new_name='Image',
        ),
    ]
