# Generated by Django 4.2.5 on 2024-03-11 04:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0043_deliverystatus"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deliverystatus",
            name="status",
            field=models.CharField(default="pending", max_length=50),
        ),
    ]
