from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegistrationPage.as_view(), name="sign_up"),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name="activate"),
    path('login/', views.LoginView.as_view(), name="login"),
]
