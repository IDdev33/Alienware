# Generated by Django 4.1.7 on 2023-05-08 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_product_reviews_score_product_reviews_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='productcolor',
            name='product',
        ),
        migrations.RemoveField(
            model_name='product',
            name='colors',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='ProductColor',
        ),
    ]