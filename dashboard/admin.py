from django.contrib import admin
from .models import Result

# Add the result table of the dataset to the admin page
admin.site.register(Result)
