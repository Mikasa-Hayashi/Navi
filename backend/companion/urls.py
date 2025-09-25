from django.urls import path
from . import views

app_name = 'companions'

urlpatterns = [
    path('', views.CompanionListView.as_view(), name='companion_list'),
    path('<int:companion_id>', views.CompanionDetailView.as_view(), name='companion_detail'),
    path('create/', views.create_companion, name='create'),
]