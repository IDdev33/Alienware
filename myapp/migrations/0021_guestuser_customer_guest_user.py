# Generated by Django 4.1.7 on 2023-05-29 18:04

from django.db import migrations, models
import django.db.models.deletion
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_orderitem_action'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(default=myapp.models.generate_guest_identifier, max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='guest_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.guestuser'),
        ),
    ]
