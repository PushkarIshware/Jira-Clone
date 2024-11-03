import jwt
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from jwt.exceptions import InvalidSignatureError

User = get_user_model()

class CustomJWTTokenAuthentication(BasePermission):
    invalid_token_msg = 'Invalid token. Please provide a valid JWT token.'
    token_missing_msg = 'JWT token is missing'
    def has_permission(self, request, view):
        
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if not jwt_token:
            raise AuthenticationFailed(detail={'message': self.token_missing_msg})
        try:
            payload = jwt.decode(jwt_token, settings.JWT_TOKEN_SECRET_NAME, algorithms=settings.JWT_TOKEN_ALGORITHM)
            # user = authenticate(username=payload['email'], ) #password=payload['password']
            user_present = User.objects.get(email=payload['email'])
            request.user=user_present
            return True
        except (AuthenticationFailed, InvalidSignatureError):
            raise AuthenticationFailed(detail={'message': self.invalid_token_msg})