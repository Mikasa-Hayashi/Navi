from django.urls import path
from . import views

app_name = 'companion'

urlpatterns = [
    path('<int:companion_id>', views.CompanionDetailView.as_view(), name='companion_detail'),
    path('create/', views.create_companion, name='create'),
]