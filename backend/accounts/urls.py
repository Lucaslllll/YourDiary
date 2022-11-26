from django.urls import path
from rest_framework import routers
from .api import UserViewSet
from rest_framework.authtoken import views
    

router = routers.DefaultRouter()
# router = routers.SimpleRouter()


router.register('users', UserViewSet, 'users')


urlpatterns = router.urls