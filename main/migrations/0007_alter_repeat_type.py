# Generated by Django 3.2.25 on 2024-07-20 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20220825_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repeat',
            name='type',
            field=models.CharField(choices=[('DAY', 'DAY'), ('WEEK', 'WEEK'), ('MONTH', 'MONTH'), ('YEAR', 'YEAR'), ('EOEM', 'EOEM')], max_length=15),
        ),
    ]