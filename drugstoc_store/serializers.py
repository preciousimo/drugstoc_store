from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import UserSerializer
from users.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token obtain pair serializer to add user_id claim to the token.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id  # Add the user_id claim
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Custom token refresh serializer to add user object to the response.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])

        # Retrieve user using the user_id claim
        user = User.objects.get(id=refresh['user_id'])
        data['user'] = UserSerializer(user).data

        return data