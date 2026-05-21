from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from .models import PCController
from .serializers import RegisterSerializer, PCControllerSerializer
from .permissions import IsVerifiedUser
from django.contrib.auth.models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Account created. Awaiting admin verification."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FrontendControllerView(APIView):
    # Only authenticated AND active users can view/change state
    permission_classes = [IsAuthenticated, IsVerifiedUser]

    def get(self, request):
        controller, _ = PCController.objects.get_or_create(id=1)
        serializer = PCControllerSerializer(controller)
        return Response(serializer.data)

    def post(self, request):
        controller, _ = PCController.objects.get_or_create(id=1)
        # Allows you to toggle the boolean 'is_permitted' 
        serializer = PCControllerSerializer(controller, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ESP32PingView(APIView):
    permission_classes = [AllowAny] # Simple approach; add Token auth if encryption is needed later

    def get(self, request):
        controller, _ = PCController.objects.get_or_create(id=1)
        
        # Fresh timestamp registration updates online status
        controller.last_seen_by_esp = timezone.now()
        
        # Capture the permission bit to send back before updating values
        permission_signal = 1 if controller.is_permitted else 0
        
        # Auto-reset pattern: Once read, clear permission back to 0 so it won't repeatedly trigger power cycles
        if controller.is_permitted:
            controller.is_permitted = False
            
        controller.save()

        return Response({"status": permission_signal})