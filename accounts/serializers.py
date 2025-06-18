import string
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        username = attrs.get('username', None)
        if '@' in username:
            self.username_field = 'email'
        elif username.isdigit():
            self.username_field = 'phone_number'
        else:
            self.username_field = 'username'

        try:
            user = User.objects.get(**{self.username_field: username})
            attrs['username'] = user.username
        except User.DoesNotExist:
            raise serializers.ValidationError("No account found with the given credentials.")

        data = super().validate(attrs)
        return data


def validate_password_strength(password):
    if len(password) < 10:
        raise serializers.ValidationError("Password must be more than 10 characters.")
    if not any(char in string.ascii_uppercase for char in password):
        raise serializers.ValidationError("Password must contain at least 1 uppercase letter.")
    if not any(char in string.ascii_lowercase for char in password):
        raise serializers.ValidationError("Password must contain at least 1 lowercase letter.")
    if not any(char in string.digits for char in password):
        raise serializers.ValidationError("Password must contain at least 1 digit.")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        validate_password_strength(value)
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("اکانتی با این نام کاربری وجود دارد.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("اکانتی با این نام ایمیل وجود دارد.")
        return value

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("اکانتی با این نام شماره وجود دارد.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance