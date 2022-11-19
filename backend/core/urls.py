from django.urls import path
from rest_framework import routers
from .api import CategoryViewSet
from rest_framework.authtoken import views
    

router = routers.DefaultRouter()
# router = routers.SimpleRouter()


router.register('categories', CategoryViewSet, 'categories')


urlpatterns = router.urls