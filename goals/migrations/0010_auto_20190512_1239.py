# Generated by Django 2.0.3 on 2019-05-12 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0009_auto_20190512_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cumulative_goal',
            name='chunk_size',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='cumulative_goal',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]