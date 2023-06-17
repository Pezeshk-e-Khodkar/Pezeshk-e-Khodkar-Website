from django.urls import path
from . import views


urlpatterns = [
    path('app/dashboard/', views.DashboardView.as_view(), name="dashboard"),  # Dashboard
    path('app/dashboard/new', views.CreateNewView.as_view(), name="create-new"),  # Create new page
    path('app/dashboard/delete/<image_id>', views.DeleteImageView.as_view(), name="delete-image")  # Delete an image
]