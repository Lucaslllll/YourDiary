from django.urls import path
from rest_framework import routers
from .api import CategoryViewSet, AnnotationViewSet, AnnotationByAuthor, AnnotationPublic
from rest_framework.authtoken import views
    

# router = routers.DefaultRouter()
router = routers.SimpleRouter()


router.register('categories', CategoryViewSet, 'categories')
router.register('annotations', AnnotationViewSet, 'annotations')


urlpatterns = router.urls


urlpatterns += [
    path('annotations/by/author/<int:pk>', AnnotationByAuthor.as_view(), name='annotation_author'),
    path('annotations/public', AnnotationPublic.as_view(), name='annotation_public'),
    
]