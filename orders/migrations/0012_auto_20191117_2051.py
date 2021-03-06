# Generated by Django 2.2.6 on 2019-11-18 02:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0011_dish_num_toppings'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='items', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='size',
            field=models.CharField(choices=[('large', 'LG'), ('small', 'SM')], max_length=2),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
