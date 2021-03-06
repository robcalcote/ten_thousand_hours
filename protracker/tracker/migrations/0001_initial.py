# Generated by Django 2.2.6 on 2020-06-11 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='description of goal')),
                ('hours', models.SmallIntegerField(verbose_name='amount of hours in goal')),
                ('hours_remaining', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='hours remaining')),
                ('created_date', models.DateTimeField(verbose_name='date created')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('achieved_date', models.DateTimeField(verbose_name='date achieved')),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.SmallIntegerField(verbose_name='amount of hours in milestone')),
                ('hours_remaining', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='hours remaining')),
                ('created_date', models.DateTimeField(verbose_name='date created')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('achieved_date', models.DateTimeField(verbose_name='date achieved')),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Goal')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='date of session')),
                ('hour_count', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='amount of hours')),
                ('difficulty', models.CharField(choices=[('1', 'Very Easy'), ('2', 'Easy'), ('3', 'Moderate'), ('4', 'Hard'), ('5', 'Very Hard')], db_index=True, default='3', max_length=1, verbose_name='difficulty level')),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tracker.Goal')),
                ('milestone', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tracker.Milestone')),
            ],
        ),
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='description of reward')),
                ('created_date', models.DateTimeField(verbose_name='date created')),
                ('rewarded_date', models.DateTimeField(verbose_name='date rewarded')),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Goal')),
                ('milestone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Milestone')),
            ],
        ),
    ]
