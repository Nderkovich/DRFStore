# Generated by Django 3.1.3 on 2020-11-04 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20201104_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(choices=[('Client', 'Client'), ('Admin', 'Admin')], max_length=10),
        ),
    ]