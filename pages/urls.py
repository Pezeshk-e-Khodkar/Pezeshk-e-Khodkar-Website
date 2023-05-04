from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),           # Home Page
    path('help/', views.HelpPage.as_view(), name="help-page")  # Help Page
]
