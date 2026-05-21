from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PCController

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        # Create user with is_active=False so superuser approval is required
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            is_active=False  # Requires Admin Approval
        )
        return user

class PCControllerSerializer(serializers.ModelSerializer):
    is_online = serializers.BooleanField(source='is_esp_online', read_only=True)

    class Meta:
        model = PCController
        fields = ['id', 'name', 'is_permitted', 'is_online', 'last_seen_by_esp']