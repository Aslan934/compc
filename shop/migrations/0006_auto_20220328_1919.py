# Generated by Django 3.1.5 on 2022-03-28 15:19

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', unique=True),
        ),
    ]
