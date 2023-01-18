from django.urls import path
from rest_framework import routers
from .api import UserViewSet, LoginAPI, MessagesAPI, MessagesCreateAPI, ChatAPI
from .api import ProfileAPI, ProfilesCreateAPI
from rest_framework.authtoken import views
    

# router = routers.DefaultRouter()
router = routers.SimpleRouter()


router.register('users', UserViewSet, 'users')


urlpatterns = router.urls

urlpatterns += [
    path('login/', LoginAPI.as_view(), name='login'),
    path('messages/', MessagesAPI.as_view(), name='messages'),
    path('messages/create/', MessagesCreateAPI.as_view(), name='message_create'),
    path('chat/', ChatAPI.as_view(), name='chat'),
    path('profiles/<int:pk>/', ProfileAPI.as_view(), name='profile'),
    path('profiles/create/<int:pk>/', ProfilesCreateAPI.as_view(), name='profile_create'),


]