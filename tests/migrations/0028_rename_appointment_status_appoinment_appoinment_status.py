# Generated by Django 4.2.5 on 2024-01-25 04:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0027_appoinment_appointment_status_appoinment_report_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="appoinment",
            old_name="appointment_status",
            new_name="appoinment_status",
        ),
    ]