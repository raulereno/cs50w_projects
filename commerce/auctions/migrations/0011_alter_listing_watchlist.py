# Generated by Django 4.1.5 on 2023-01-15 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_listing_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.watchlist'),
        ),
    ]