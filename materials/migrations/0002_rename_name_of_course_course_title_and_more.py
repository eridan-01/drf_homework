# Generated by Django 5.0.7 on 2024-07-20 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="course",
            old_name="name_of_course",
            new_name="title",
        ),
        migrations.RenameField(
            model_name="lesson",
            old_name="name",
            new_name="title",
        ),
    ]
