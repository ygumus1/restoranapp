# Generated by Django 5.0.2 on 2024-05-28 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_rename_is_cancelled_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerprofile',
            name='account_type',
            field=models.CharField(default='Customer', max_length=20),
        ),
        migrations.AddField(
            model_name='restaurantprofile',
            name='account_type',
            field=models.CharField(default='Restaurant', max_length=20),
        ),
    ]
