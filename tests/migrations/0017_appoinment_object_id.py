# Generated by Django 4.2.5 on 2023-11-05 06:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0016_appoinment_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="appoinment",
            name="object_id",
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]
