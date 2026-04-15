from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import authenticate
from django.conf import settings


REFRESH_COOKIE_NAME = 'refreshToken'
REFRESH_COOKIE_MAX_AGE = 60 * 60 * 24 * 30  # 30 days


def _is_secure_cookie():
    return not settings.DEBUG


def _same_site_policy():
    return 'None' if _is_secure_cookie() else 'Lax'


def _set_refresh_cookie(response, refresh_token, remember_me=False):
    cookie_kwargs = {
        'key': REFRESH_COOKIE_NAME,
        'value': refresh_token,
        'httponly': True,
        'secure': _is_secure_cookie(),
        'samesite': _same_site_policy(),
        'path': '/',
    }
    if remember_me:
        cookie_kwargs['max_age'] = REFRESH_COOKIE_MAX_AGE
    response.set_cookie(**cookie_kwargs)

# Create your views here.
class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if not user.is_active:
                raise AuthenticationFailed('User is deactivated')
            
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                'user_id': user.id,
                'username': user.username,
                'date_joined': user.date_joined.isoformat(),
            })

            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({
                'accessToken': access_token,
            }, status=status.HTTP_201_CREATED)

            _set_refresh_cookie(response, refresh_token, remember_me=True)

            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        remember_me = bool(request.data.get('rememberMe', False))

        if username is None or password is None:
            return Response({
                'error': 'Username and password required',
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed('Invalid credentials')
        
        if not user.is_active:
            raise AuthenticationFailed('User is deactivated')
    
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username,
            'date_joined': user.date_joined.isoformat(),
        })
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({
            'accessToken': access_token,
        }, status=status.HTTP_200_OK)

        _set_refresh_cookie(response, refresh_token, remember_me=remember_me)

        return response
        

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(
            key=REFRESH_COOKIE_NAME,
            path='/',
            samesite=_same_site_policy(),
        )
        return response


class CookieTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get(REFRESH_COOKIE_NAME)
        if refresh_token is None:
            return Response({'error': 'Refresh token not provided;'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)

            access_token = str(refresh.access_token)

            return Response({
                'accessToken': access_token,
            }, status=status.HTTP_200_OK)
        except InvalidToken:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)



def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('chat:conversation_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', { 'form': form })

def log_in_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.POST.get('next', 'chat:conversation_list'))
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', { 'form': form })

def log_out_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('users:login')