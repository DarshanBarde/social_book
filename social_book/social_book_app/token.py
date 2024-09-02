from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Token

class TokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('No token provided')

        try:
            token = token.split(' ')[1]
            user = Token.objects.get(key=token).user
            return (user, token)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token')