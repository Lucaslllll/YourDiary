from django.urls import path
from rest_framework import routers
from .api import UserViewSet, LoginAPI, MessagesAPI, MessagesCreateAPI, ChatAPI
from .api import ProfileViewSet, ProfileAPI, FollowingAPI, SendEmailAPI
from .api import RedefinePasswordAPI, ConfirmePasswordAPI

    

# router = routers.DefaultRouter()
router = routers.SimpleRouter()


router.register('users', UserViewSet, 'users')
router.register('profiles', ProfileViewSet, 'profiles')

urlpatterns = router.urls

urlpatterns += [
    path('login/', LoginAPI.as_view(), name='login'),
    path('messages/', MessagesAPI.as_view(), name='messages'),
    path('messages/create/', MessagesCreateAPI.as_view(), name='message_create'),
    path('chat/', ChatAPI.as_view(), name='chat'),
    path('profiles/check/<int:pk>', ProfileAPI.as_view(), name='profiles_check'),
    path('followings/<int:pk>', FollowingAPI.as_view(), name='followings'),
    path('email/send/', SendEmailAPI.as_view(), name='send email'),
    path('password/redefine/', RedefinePasswordAPI.as_view(), name='Redefine Password'),
	path('password/redefine/confirme/<str:token>/', ConfirmePasswordAPI.as_view(), name='Confirme Password')

]