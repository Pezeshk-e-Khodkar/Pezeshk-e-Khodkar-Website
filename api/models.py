from django.db import models


class Result(models.Model):
    disease_type = models.CharField(max_length=100)
    signature = models.CharField(max_length=64)
    result = models.TextField()
