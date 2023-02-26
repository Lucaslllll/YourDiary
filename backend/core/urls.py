from django.urls import path
from rest_framework import routers
from .api import CategoryViewSet, AnnotationViewSet, AnnotationByAuthor, AnnotationPublic
from .api import FavoriteViewSet, FavoriteAPI, FavoriteCheckAPI, ReportViewSet, LikeViewSet
from .api import LikeCheckAPI
from rest_framework.authtoken import views
from .views import politic_privacy, terms_of_use

# router = routers.DefaultRouter()
router = routers.SimpleRouter()


router.register('categories', CategoryViewSet, 'categories')
router.register('annotations', AnnotationViewSet, 'annotations')
router.register('favorites', FavoriteViewSet, 'favorites')
router.register('reports', ReportViewSet, 'reports')
router.register('likes', LikeViewSet, 'likes')

urlpatterns = router.urls


urlpatterns += [
    path('annotations/by/author/<int:pk>', AnnotationByAuthor.as_view(), name='annotation_author'),
    path('annotations/public', AnnotationPublic.as_view(), name='annotation_public'),
    path('annotations/favorites/<int:pk>', FavoriteAPI.as_view(), name='annotations_favorites'),
    path('annotations/favorites/check/', FavoriteCheckAPI.as_view(), name='annotations_favorites_check'),
    path('annotations/likes/check/', LikeCheckAPI.as_view(), name='annotations_likes_check'),
    path('sobre/politica/privacidade', politic_privacy, name='politic_privacy'),
    path('sobre/termos/uso', terms_of_use, name='terms_of_use'),
]