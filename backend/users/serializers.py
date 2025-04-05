from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Profile  # Import Profile model

User = get_user_model()  # Use CustomUser model correctly

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    """Serializer for CustomUser model."""

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number', 'role']  # No 'username' field

# Custom Token Serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer for JWT token to include additional user details."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email  # Include email in token payload
        token['role'] = user.role  # Include user role in token
        return token

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model with nested User data."""
    
    user = UserSerializer(read_only=True)  #  Include user data

    class Meta:
        model = Profile
        fields = '__all__'  #  Serialize all fields

#  Custom Register Serializer (Fixes the missing username issue)
class CustomRegisterSerializer(RegisterSerializer):
    """Custom registration serializer that removes username and relies on email."""

    username = None  #  Remove username
    email = serializers.EmailField(required=True)  #  Ensure email is required

    def get_cleaned_data(self):
        """Ensure necessary fields are captured properly."""
        return {
            "email": self.validated_data.get("email", ""),
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
        }

    def save(self, request):
        """Override save to ensure user creation without username."""
        user = User(email=self.validated_data.get("email"))
        user.set_password(self.validated_data.get("password1"))
        user.save()
        return user
