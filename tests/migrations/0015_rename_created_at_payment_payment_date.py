# Generated by Django 4.2.5 on 2023-11-05 06:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0014_paymentdetail_payment"),
    ]

    operations = [
        migrations.RenameField(
            model_name="payment",
            old_name="created_at",
            new_name="payment_date",
        ),
    ]
