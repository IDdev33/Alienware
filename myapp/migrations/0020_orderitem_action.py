# Generated by Django 4.1.7 on 2023-05-27 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_rename_address_profile_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='action',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
