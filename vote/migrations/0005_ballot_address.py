# Generated by Django 2.0.13 on 2019-11-14 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_auto_20191106_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='ballot',
            name='address',
            field=models.TextField(default='0x', verbose_name='Ethereum address'),
        ),
    ]