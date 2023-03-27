from django.urls import path
from . import views

urlpatterns = [
    path("", views.APIPage.as_view()),
]
