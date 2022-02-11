from django.db import models


class LanguageApply(models.Model):
    language_id = models.IntegerField()
    applied = models.BooleanField(default=False)
