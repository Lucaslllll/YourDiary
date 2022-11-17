from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User, Category, Annotation, Like
from .serializers import CategorySerializer





class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


