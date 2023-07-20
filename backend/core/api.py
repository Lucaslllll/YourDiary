from django.db.models import Q
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .models import User, Category, Annotation, Like, Comment, Favorite, Report
from .models import AnnotationImage
from .serializers import CategorySerializer, AnnotationSerializer, CommentSerializer
from .serializers import FavoriteSerializer, FavoriteCheckSerializer, ReportSerializer
from .serializers import LikeSerializer, LikeCheckSerializer, AnnotationImageSerializer
from .serializers import AnnotationCryptSerializer, SearchSerializer

from .utils import LargeResultsSetPagination, StandardResultsSetPagination




class CategoryViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, )
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'head']


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


class AnnotationImageViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, )
    queryset = AnnotationImage.objects.all()
    serializer_class = AnnotationImageSerializer
    pagination_class = StandardResultsSetPagination
    http_method_names = ['post', 'patch', 'get', 'head', 'options']


class ImageByAnnotation(generics.ListAPIView):
    serializer_class = AnnotationImageSerializer
    # permission_classes = (IsAuthenticated, )
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        annotation = self.kwargs['pk']
        return AnnotationImage.objects.filter(annotation=annotation)


class SearchAPI(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = SearchSerializer
    queryset = Annotation.objects.all()
    pagination_class = StandardResultsSetPagination

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.data['text']
        data = Annotation.objects.filter(Q(name__icontains=text) | Q(text__icontains=text) | Q(preview__icontains=text), public=False).values()

        return Response({"results":data})



class FavoriteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    pagination_class = StandardResultsSetPagination


class FavoriteAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnotationSerializer
    pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        user_ob = User.objects.get(pk=self.kwargs['pk'])
        lista = [favorite.annotation.pk for favorite in Favorite.objects.filter(user=user_ob).order_by("-date")]

        return Annotation.objects.filter(pk__in=lista)

class FavoriteCheckAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = FavoriteCheckSerializer
    queryset = Favorite.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"results": serializer.data })


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



class ReportViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    http_method_names = ['post', 'head']

class LikeViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated, )
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    http_method_names = ['post', 'get', 'delete', 'head']


class LikeCheckAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = LikeCheckSerializer
    queryset = Like.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"results": serializer.data })
