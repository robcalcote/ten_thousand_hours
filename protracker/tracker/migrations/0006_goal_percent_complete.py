# Generated by Django 3.0.7 on 2020-08-20 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20200620_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='percent_complete',
            field=models.DecimalField(decimal_places=3, max_digits=5, null=True, verbose_name='percentage complete'),
        ),
    ]