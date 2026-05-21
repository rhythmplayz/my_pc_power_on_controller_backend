from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from .models import DeviceControlState

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password.")
            if not user.is_active:
                raise serializers.ValidationError("This user account is disabled.")
            
            # --- ADD THIS CHECK ---
            if not user.is_verified:
                raise serializers.ValidationError("Your account is pending verification by an administrator.")

        data["user"] = user
        return data
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'email': {'required': False, 'allow_blank': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields must match."})
        return attrs

    def create(self, validated_data):
        # Remove the confirmation field before creation
        validated_data.pop('password_confirm')
        
        # Create the user using create_user to ensure the password gets properly hashed
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
    
class DeviceControlStateSerializer(serializers.ModelSerializer):
    # Read-only fields computed by the backend
    is_esp32_online = serializers.ReadOnlyField()
    last_heartbeat = serializers.DateTimeField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DeviceControlState
        fields = ['user', 'should_power_on', 'is_esp32_online', 'last_heartbeat']