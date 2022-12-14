from django.urls import path
from rest_framework import routers
from .api import UserViewSet, LoginAPI
from rest_framework.authtoken import views
    

router = routers.DefaultRouter()
# router = routers.SimpleRouter()


router.register('users', UserViewSet, 'users')


urlpatterns = router.urls

urlpatterns += [
    path('login/', LoginAPI.as_view(), name='login'),
    
]