from django.db import models


class Result(models.Model):
    """Result table of dataset
    params:
        - disease_type: Type of disease
        - signature: Signature of image
        - result: Results as a dictionary
    """
    disease_type = models.CharField(max_length=100)
    signature = models.CharField(max_length=64)
    result = models.TextField()
