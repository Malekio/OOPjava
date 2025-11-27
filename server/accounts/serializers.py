from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone_number', 'user_type'
        )
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Password fields didn\'t match.'
            })
        
        # Remove password_confirm from validated data
        attrs.pop('password_confirm')
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email already exists.')
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('User with this username already exists.')
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        
        # Create corresponding profile based on user type
        if user.user_type == 'tourist':
            from profiles.models import TouristProfile
            TouristProfile.objects.create(user=user)
        elif user.user_type == 'guide':
            from profiles.models import GuideProfile
            # Guide profiles need additional required fields, will be created via separate endpoint
            pass
        
        return user

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password.')
        
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile data
    """
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'user_type', 'is_verified', 'date_joined'
        )
        read_only_fields = ('id', 'username', 'user_type', 'is_verified', 'date_joined')

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile
    """
    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'phone_number'
        )
    
    def validate_email(self, value):
        user = self.instance
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError('User with this email already exists.')
        return value

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer with additional user data
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add user info to token response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'user_type': self.user.user_type,
            'is_verified': self.user.is_verified,
        }
        
        return data

# Alias for backwards compatibility
UserSerializer = UserProfileSerializer
