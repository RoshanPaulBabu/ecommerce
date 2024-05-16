# Generated by Django 5.0.4 on 2024-05-11 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0010_purchaseorder_purchaseorderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorderitem',
            name='TotalAmount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='ExpectedDeliveryDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='Status',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='TotalAmount',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='PurchaseUnitPrice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]