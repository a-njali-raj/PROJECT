# Generated by Django 4.2.5 on 2024-01-22 16:44

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0025_rename_result_results"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Results",
            new_name="Report",
        ),
    ]
