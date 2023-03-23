from django.urls import path
from . import views

urlpatterns = [
    path("ASD/", views.AutomatedSkinCancerDetectorPage.as_view()),
]