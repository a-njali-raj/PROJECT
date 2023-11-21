# Generated by Django 4.2.5 on 2023-11-18 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0018_alter_appoinment_object_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="RazorPayInvoice",
            fields=[
                (
                    "id",
                    models.CharField(
                        editable=False, max_length=20, primary_key=True, serialize=False
                    ),
                ),
                ("receipt", models.CharField(max_length=20, unique=True)),
                ("data", models.JSONField()),
            ],
        ),
        migrations.RemoveField(
            model_name="payment",
            name="detail",
        ),
        migrations.DeleteModel(
            name="PaymentDetail",
        ),
        migrations.AddField(
            model_name="payment",
            name="invoice",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="tests.razorpayinvoice",
            ),
        ),
    ]
