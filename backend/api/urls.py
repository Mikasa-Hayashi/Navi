from django.urls import path, include

urlpatterns = [
    path('users/', include('users.urls')),
    path('chat/', include('chat.urls')),
    path('companion/', include('companion.urls')),
]