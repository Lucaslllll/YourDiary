from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.hashers import make_password, check_password

from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    queryset = User.objects.all()
    serializer_class = UserSerializer
