from rest_framework.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            return None
        try:
            validated_token = self.get_validated_token(raw_token)
        except AuthenticationFailed as e:
            raise AuthenticationFailed(f' Invalid token: {str(e)}')
        
        try: 
            user = self.get_user(validated_token)
        except AuthenticationFailed as e:
            raise AuthenticationFailed(f'Error retrieving user: {str(e)}')
        # csrf enforcement can be added here if needed
        return user, validated_token
        