# Generated by Django 4.2.5 on 2023-11-04 12:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0009_remove_user_last_login"),
    ]

    operations = [
        migrations.AddField(
            model_name="appoinment",
            name="prescription",
            field=models.FileField(
                blank=True, null=True, upload_to="media/prescriptions/"
            ),
        ),
    ]
