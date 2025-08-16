from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import update_last_login
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        response_data = {
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'User registered successfully. Please check your email for login credentials.'
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)


from rest_framework_simplejwt.views import TokenObtainPairView

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Get the user based on the username from the request
            username = request.data.get('username')
            try:
                user = User.objects.get(username=username)
                response.data['user'] = UserSerializer(user).data
                response.data['message'] = 'Login successful.'
            except User.DoesNotExist:
                pass
                
        return response

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]  # Use JWT authentication

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_serializer_context(self):
        return {'request': self.request}