# Generated by Django 4.2.5 on 2024-02-10 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0035_address_full_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="tests.address",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="total_amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]