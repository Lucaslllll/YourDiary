from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import User, Category, Annotation, Like
from .serializers import CategorySerializer, AnnotationSerializer
from .utils import LargeResultsSetPagination, StandardResultsSetPagination




class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class AnnotationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    pagination_class = StandardResultsSetPagination


class AnnotationByAuthor(generics.ListAPIView):
    serializer_class = AnnotationSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        author = self.kwargs['pk']
        return Annotation.objects.filter(author=author)