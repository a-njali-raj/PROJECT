# Generated by Django 4.2.5 on 2023-11-04 10:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tests", "0007_alter_user_options_remove_user_date_joined_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_superuser",
            field=models.BooleanField(
                default=False,
                help_text="Designates that this user has all permissions without explicitly assigning them.",
                verbose_name="Superuser status",
            ),
        ),
    ]
