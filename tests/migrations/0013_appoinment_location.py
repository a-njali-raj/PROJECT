# Generated by Django 4.2.5 on 2023-11-05 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0012_alter_location_distance"),
    ]

    operations = [
        migrations.AddField(
            model_name="appoinment",
            name="location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="tests.location",
            ),
        ),
    ]
