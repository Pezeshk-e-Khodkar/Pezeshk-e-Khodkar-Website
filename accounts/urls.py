from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.RegistrationPage.as_view(), name="sign_up"),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name="activate"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('password_reset/', views.ResetPasswordView.as_view(), name="reset_password"),
    path('password_reset/<uidb64>/<token>/',
         views.ChangePasswordView.as_view(), name="change_password"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
]
