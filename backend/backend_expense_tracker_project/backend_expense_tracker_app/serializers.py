from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Expense
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    """Serializes user information (excluding password)"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

class RegisterSerializer(serializers.ModelSerializer):
    """Handles user registration and returns JWT token"""
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'token']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Creates a new user and returns JWT token"""
        user = User.objects.create_user(**validated_data)
        return user

    def get_token(self, obj):
        """Generates JWT token upon successful registration"""
        refresh = RefreshToken.for_user(obj)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

class ExpenseSerializer(serializers.ModelSerializer):
    """Serializes expense data"""
    category = serializers.ChoiceField(choices=Expense.CATEGORY_CHOICES)

    class Meta:
        model = Expense
        exclude = ['user']  # ✅ Auto-assign user from request

    def create(self, validated_data):
        """Ensures expenses are linked to the logged-in user"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
