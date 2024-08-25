# serializers.py
from rest_framework import serializers
from .models import CustomUser
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model, handling user data serialization and deserialization.

    Methods:
        update(instance, validated_data):
            Updates a CustomUser instance with validated data, handling password separately.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'initials', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'initials' : {'read_only' : True}}

    def update(self, instance, validated_data):
        """
        Update an existing CustomUser instance with the provided validated data.

        Returns:
            CustomUser: The updated user instance.
        """
        for attr, value in validated_data.items():
            if attr == 'password':
                # hash password
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
    
    
    
class CustomAuthTokenSerializer(serializers.Serializer):
    """
    Serializer for handling user authentication tokens.

    Fields:
        email (str): The email address of the user (write-only).
        password (str): The user's password (write-only).
        token (str): The authentication token (read-only).

    Methods:
        validate(attrs):
            Validates the provided credentials and authenticates the user.
    """
    
    email = serializers.EmailField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        """
        Validate the provided email and password, and authenticate the user.
        """
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs



class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    Fields:
        username (str): The username for the new user.
        email (str): The email address for the new user.
        password (str): The password for the new user (write-only).

    Methods:
        create(validated_data):
            Creates a new CustomUser instance with the validated data.
    """
    class Meta: 
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password' : {'write_only' : True}}
      
  
    def create(self, validated_data):
        """
        Create a new CustomUser instance with the provided validated data.

        Returns:
            CustomUser: The newly created user instance.
        """
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = CustomUser.objects.create_user(email=email, password=password, username=username)
        return user
    
    