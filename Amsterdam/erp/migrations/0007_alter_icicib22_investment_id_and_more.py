# Generated by Django 4.0.3 on 2023-04-19 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0006_rename_icicib50_investment_icicib22_investment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icicib22_investment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='icicib22_profit',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='nasdaq100_investment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='nasdaq100_profit',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]