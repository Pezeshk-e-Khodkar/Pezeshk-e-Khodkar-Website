# Urls of this app
from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name="sign_up"),  # Register page
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name="activate"),  # Activation pages
    path('login/', views.LoginView.as_view(), name="login"),  # Login page
    path('password_reset/', views.ResetPasswordView.as_view(), name="reset_password"),  # Reset password page
    path('password_reset/<uidb64>/<token>/',  # Change aassword pages
         views.ChangePasswordView.as_view(), name="change_password"),
    path('logout/', views.LogoutView.as_view(), name="logout"),  # Logout page
]
