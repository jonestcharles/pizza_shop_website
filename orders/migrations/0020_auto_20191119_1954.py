# Generated by Django 2.2.6 on 2019-11-20 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.IntegerField(blank=True, default=-1, editable=False, null=True),
        ),
    ]
