from django.contrib import admin
from .models import Result

# Add result table of dataset to admin page
admin.site.register(Result)