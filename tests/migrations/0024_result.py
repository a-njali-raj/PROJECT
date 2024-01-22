# Generated by Django 4.2.5 on 2024-01-22 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0023_review"),
    ]

    operations = [
        migrations.CreateModel(
            name="Result",
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
                ("object_id", models.UUIDField(default=uuid.uuid4, unique=True)),
                (
                    "uploaded_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "result_file",
                    models.FileField(blank=True, null=True, upload_to="media/results/"),
                ),
                (
                    "appoinment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tests.appoinment",
                    ),
                ),
                (
                    "uploaded_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
