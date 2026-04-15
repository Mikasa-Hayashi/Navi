from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logout/form/', views.log_out_user, name='logout_form'),
    path('token/refresh', views.CookieTokenRefreshView.as_view(), name='token_refresh'),
]