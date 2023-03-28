from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.utils import datetime_to_epoch
from rest_framework_simplejwt.tokens import RefreshToken

import datetime

from .models import (
    User,
    Instructor,
    Learner
)

SUPERUSER_LIFETIME = datetime.timedelta(minutes=30)


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'is_instructor', 'is_learner', 'profile')
        read_only_fields = ('is_verify', )

    def get_profile(self, obj):
        if obj.is_instructor:
            return InstructorSerializer(obj.instructor).data
        else:
            return LearnerSerializer(obj.learner).data

class CustomRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            is_instructor=validated_data["is_instructor"],
            is_learner=validated_data["is_learner"],
            password=validated_data["password"],
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'is_instructor', 'is_learner')
        read_only_fields = ('is_verify', )


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class CustomJwtLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(CustomJwtLoginSerializer, cls).get_token(user)
        token["user_id"] = user.id
        token["email"] = user.email
        token["is_instructor"] = user.is_instructor
        token["is_learner"] = user.is_learner
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser
        token["is_verify"] = user.is_verify
        
        if user:
            token.payload["exp"] = datetime_to_epoch(
                token.current_time + SUPERUSER_LIFETIME
            )
            return token


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = '__all__'
        read_only_fields = ('user',)


class LearnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Learner
        fields = '__all__'
        read_only_fields = ('user',)
