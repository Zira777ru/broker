# Generated by Django 4.1.5 on 2023-01-20 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tradingpair',
            name='price',
        ),
    ]
