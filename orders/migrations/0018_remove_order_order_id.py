# Generated by Django 2.2.6 on 2019-11-20 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_auto_20191119_1940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_id',
        ),
    ]
