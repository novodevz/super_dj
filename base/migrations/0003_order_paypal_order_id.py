# Generated by Django 5.0.1 on 2024-03-04 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paypal_order_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
