from random import choice

from django.db import models
from django.utils import timezone

from Main.models import Solution, Set
from SprintLib.utils import generate_token


class Checker(models.Model):
    token = models.CharField(max_length=30, default=generate_token, db_index=True, unique=True)
    dynamic_token = models.CharField(max_length=30, default=generate_token, db_index=True, unique=True)
    testing_solution = models.ForeignKey(Solution, on_delete=models.SET_NULL, null=True)
    set = models.ForeignKey(Set, on_delete=models.CASCADE, related_name="checkers")
    last_request = models.DateTimeField()
    name = models.CharField(max_length=50, default='')

    @property
    def status(self):
        if self.testing_solution is not None:
            return 'Testing'
        if (timezone.now() - self.last_request).total_seconds() > 3:
            return 'Disabled'
        return 'Active'
