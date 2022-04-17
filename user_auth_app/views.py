
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny


class RegisterView(APIView):
    """
    Register User with username and password.
    For Activating user AC pass is_active = 1 param in body. 
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            if serializer.is_valid():
                serializer.save(password=password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailView(APIView):
    """
    Get user details with passing user access_token in header
    eg. Authorization : Bearer {access_token}
    """
    permission_classes = (IsAuthenticated,)
    
    def get(self, request,format=None):
        if request.user.is_superuser:
            queryset = User.objects.all()
        else:
            queryset = User.objects.filter(username=request.user)
        serializer = UserSerializer(queryset,many=True)
        return Response(serializer.data)