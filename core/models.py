from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from accounts.models import CustomUser

PREFERENCES_MIN = 0
PREFERENCES_MAX = 1
MIN_ANSWER = 1
MAX_ANSWER = 3


class QuestionnaireA(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    user = models.OneToOneField(CustomUser, on_delete=models.RESTRICT)
    ml_answer = models.IntegerField(
        validators=[MinValueValidator(PREFERENCES_MIN), MaxValueValidator(PREFERENCES_MAX)]
    )
    model_answer = models.IntegerField(
        validators=[MinValueValidator(PREFERENCES_MIN), MaxValueValidator(PREFERENCES_MAX)]
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'QuestionnaireA'
        verbose_name = 'Capital Market - Algorithm Preferences'
        verbose_name_plural = 'Capital Market - Algorithm Preferences'


class QuestionnaireB(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    user = models.OneToOneField(CustomUser, on_delete=models.RESTRICT)
    answer_1 = models.IntegerField(validators=[MinValueValidator(MIN_ANSWER), MaxValueValidator(MAX_ANSWER)])
    answer_2 = models.IntegerField(validators=[MinValueValidator(MIN_ANSWER), MaxValueValidator(MAX_ANSWER)])
    answer_3 = models.IntegerField(validators=[MinValueValidator(MIN_ANSWER), MaxValueValidator(MAX_ANSWER)])
    answers_sum = models.IntegerField(validators=[MinValueValidator(MIN_ANSWER * 3), MaxValueValidator(MAX_ANSWER * 3)])
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'QuestionnaireB'
        verbose_name = 'Capital Market - Investment Preferences'
        verbose_name_plural = 'Capital Market - Investment Preferences'


class TeamMember(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    alt = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=20, unique=True)
    github_username = models.CharField(max_length=30, unique=True)
    img = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'TeamMember'
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Member'
