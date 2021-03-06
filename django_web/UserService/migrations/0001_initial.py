# Generated by Django 2.1.4 on 2019-01-04 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('arrangements', models.IntegerField(blank=True, null=True)),
                ('supply', models.IntegerField(blank=True, null=True)),
                ('max_power', models.IntegerField(blank=True, null=True)),
                ('reserve_power', models.IntegerField(blank=True, null=True)),
                ('reserve_per', models.FloatField(blank=True, null=True)),
                ('basic_date', models.DateTimeField(blank=True, null=True)),
                ('avg_tem', models.FloatField(blank=True, null=True)),
                ('avg_max_tem', models.FloatField(blank=True, null=True)),
                ('min_tem', models.FloatField(blank=True, null=True)),
                ('max_tem', models.FloatField(blank=True, null=True)),
                ('avg_min_tem', models.FloatField(blank=True, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'new_table',
                'managed': False,
            },
        ),
    ]
