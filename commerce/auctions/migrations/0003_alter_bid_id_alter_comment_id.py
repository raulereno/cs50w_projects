# Generated by Django 4.1.5 on 2023-01-15 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_comment_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
