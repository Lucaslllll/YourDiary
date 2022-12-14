from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.hashers import make_password, check_password

from .models import User
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)

        userOb = User.objects.get(username=serializer.validated_data['username'])

        return Response({

                            "id": userOb.id,
                            "first_name": userOb.first_name,
                            "last_name": userOb.last_name,
                            "email" : userOb.email,
                        
                        })