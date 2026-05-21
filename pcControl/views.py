from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import DeviceControlStateSerializer, LoginSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from .models import DeviceControlState
from django.utils import timezone

class LoginAPIView(APIView):
    """
    API View to handle user login. Returns a token upon successful authentication.
    """
    permission_classes = []  # Anyone can attempt to log in

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                "token": token.key,
                "username": user.username,
                "message": "Login successful"
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterAPIView(APIView):
    """
    API View to handle user registration. Returns user data along with an auth token.
    """
    permission_classes = []  # Publicly accessible

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                "username": user.username,
                "email": user.email,
                "token": token.key,
                "message": "User registered successfully."
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UIControlAPIView(APIView):
    """
    Endpoint for the User Interface.
    GET: Fetch the current state of the PC intent and ESP32 status.
    PATCH: Toggle 'should_power_on' true or false.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, user):
        # Automatically get or create a state row for this specific user
        state, created = DeviceControlState.objects.get_or_create(user=user)
        return state

    def get(self, request):
        state = self.get_object(request.user)
        serializer = DeviceControlStateSerializer(state)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        state = self.get_object(request.user)
        serializer = DeviceControlStateSerializer(state, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ESP32HeartbeatAPIView(APIView):
    """
    Endpoint for the ESP32 hardware client.
    POST: Updates last_heartbeat timestamp to now and returns the targets.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        state, created = DeviceControlState.objects.get_or_create(user=request.user)
        
        # Update the timestamp to the current moment
        state.last_heartbeat = timezone.now()
        state.save()
        
        # Send back the current instructions so the ESP32 knows whether to boot the PC
        serializer = DeviceControlStateSerializer(state)
        return Response({
            "should_power_on": state.should_power_on,
            "message": "Heartbeat acknowledged."
        }, status=status.HTTP_200_OK)