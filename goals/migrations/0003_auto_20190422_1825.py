# Generated by Django 2.0.3 on 2019-04-22 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_auto_20190422_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]
