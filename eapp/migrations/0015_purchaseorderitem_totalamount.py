# Generated by Django 5.0.4 on 2024-05-12 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0014_remove_purchaseorderitem_totalamount'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderitem',
            name='TotalAmount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
