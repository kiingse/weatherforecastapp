from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Cities(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=255)

    
    def __str__(self):
        return self.city

class Page(models.Model):
    visits_count = models.IntegerField()

    