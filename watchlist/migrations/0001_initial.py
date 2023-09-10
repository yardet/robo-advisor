# Generated by Django 4.2.4 on 2023-09-09 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TopStock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("sector_name", models.CharField(max_length=70)),
                ("sector_as_variable", models.CharField(max_length=70)),
            ],
            options={
                "verbose_name": "Top Stock",
                "verbose_name_plural": "Top Stock",
                "db_table": "TopStock",
                "ordering": ["sector_name"],
            },
        ),
    ]
