# Generated by Django 4.2.1 on 2023-06-04 20:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_create_permissions_2244"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="category",
            new_name="categories",
        ),
    ]
