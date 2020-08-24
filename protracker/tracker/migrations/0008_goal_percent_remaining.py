# Generated by Django 3.0.7 on 2020-08-20 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_auto_20200819_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='percent_remaining',
            field=models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='percentage remaining'),
        ),
    ]