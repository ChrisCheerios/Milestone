# Generated by Django 2.0.3 on 2019-04-27 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0006_goal_target_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cumulative_goal',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]