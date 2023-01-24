from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import User, Category, Annotation, Like, Comment, Favorite
from .serializers import CategorySerializer, AnnotationSerializer, CommentSerializer
from .serializers import FavoriteSerializer
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

class AnnotationPublic(generics.ListAPIView):
    serializer_class = AnnotationSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Annotation.objects.filter(public=True)


class FavoriteViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, )
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    pagination_class = StandardResultsSetPagination


class FavoriteAPI(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = FavoriteSerializer
    pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        user_ob = User.objects.get(pk=self.kwargs['pk'])
    
        return Favorite.objects.filter(user=user_ob).order_by("-date")


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer