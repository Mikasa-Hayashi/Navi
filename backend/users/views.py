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

            response.set_cookie(
                key='refreshToken',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
            )

            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

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

        response.set_cookie(
            key='refreshToken',
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite='None',
        )

        return response
        

class LogoutView(APIView):
    pass


class CookieTokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.COOKIES)
        refresh_token = request.COOKIES.get('refreshToken')
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