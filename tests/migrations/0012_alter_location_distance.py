# Generated by Django 4.2.5 on 2023-11-04 12:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0011_location"),
    ]

    operations = [
        migrations.AlterField(
            model_name="location",
            name="distance",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
