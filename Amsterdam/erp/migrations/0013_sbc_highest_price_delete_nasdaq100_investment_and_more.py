# Generated by Django 4.0.3 on 2023-04-30 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0012_remove_icicib22_investment_net_investment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SBC_highest_price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('high_share_price', models.FloatField()),
            ],
        ),
        migrations.DeleteModel(
            name='NASDAQ100_investment',
        ),
        migrations.DeleteModel(
            name='NASDAQ100_profit',
        ),
    ]
