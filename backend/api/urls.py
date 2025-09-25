from django.urls import path, include

urlpatterns = [
    path('users/', include('users.urls')),
    path('conversations/', include('chat.urls')),
    path('companions/', include('companion.urls')),
]