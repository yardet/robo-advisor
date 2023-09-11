# Generated by Django 4.2.5 on 2023-09-11 00:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TeamMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("alt", models.CharField(max_length=20, unique=True)),
                ("full_name", models.CharField(max_length=20, unique=True)),
                ("github_username", models.CharField(max_length=30, unique=True)),
                ("img", models.CharField(max_length=30, unique=True)),
            ],
            options={
                "verbose_name": "Team Member",
                "verbose_name_plural": "Team Member",
                "db_table": "TeamMember",
            },
        ),
        migrations.CreateModel(
            name="QuestionnaireB",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "answer_1",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(3),
                        ]
                    ),
                ),
                (
                    "answer_2",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(3),
                        ]
                    ),
                ),
                (
                    "answer_3",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(3),
                        ]
                    ),
                ),
                (
                    "answers_sum",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(3),
                            django.core.validators.MaxValueValidator(9),
                        ]
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Capital Market - Investment Preferences",
                "verbose_name_plural": "Capital Market - Investment Preferences",
                "db_table": "QuestionnaireB",
            },
        ),
        migrations.CreateModel(
            name="QuestionnaireA",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "ml_answer",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1),
                        ]
                    ),
                ),
                (
                    "model_answer",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1),
                        ]
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Capital Market - Algorithm Preferences",
                "verbose_name_plural": "Capital Market - Algorithm Preferences",
                "db_table": "QuestionnaireA",
            },
        ),
    ]
