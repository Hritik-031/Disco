# Generated by Django 4.0.3 on 2023-05-04 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0013_sbc_highest_price_delete_nasdaq100_investment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ICICIB22_highest_price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('high_share_price', models.FloatField()),
            ],
        ),
    ]