from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.log_out_user, name='logout'),
    path('token/refresh', views.CookieTokenRefreshView.as_view(), name='token_refresh'),
]