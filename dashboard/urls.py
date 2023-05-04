from django.urls import path
from . import views


urlpatterns = [
    path('app/dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('app/dashboard/new', views.CreateNewView.as_view(), name="create-new"),
    path('app/dashboard/delete/<image_id>', views.DeleteImageView.as_view(), name="delete-image")
]