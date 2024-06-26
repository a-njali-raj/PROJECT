# Generated by Django 4.2.5 on 2024-02-05 15:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0029_rename_appoinment_status_appoinment_appointment_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_name", models.CharField(max_length=50)),
                ("product_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("brand", models.CharField(max_length=100)),
                ("is_available", models.BooleanField(default=True)),
                (
                    "product_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="product_images/"
                    ),
                ),
                ("discount", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "product_sale_price",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("stock", models.IntegerField(default=0)),
            ],
        ),
    ]
