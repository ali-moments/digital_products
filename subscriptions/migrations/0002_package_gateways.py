# Generated by Django 4.2.4 on 2023-09-03 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_payment_package'),
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='gateways',
            field=models.ManyToManyField(to='payments.gateway'),
        ),
    ]
