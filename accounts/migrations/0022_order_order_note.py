# Generated by Django 5.0.2 on 2024-05-10 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_rename_customer_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
