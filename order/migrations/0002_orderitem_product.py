# Generated by Django 3.1.5 on 2022-03-19 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='shop.product'),
        ),
    ]
