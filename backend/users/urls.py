from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.log_in_user, name='login'),
    path('logout/', views.log_out_user, name='logout'),
]