from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.hashers import make_password, check_password

from .models import User, Message, Profile
from core.models import Annotation
from .serializers import UserSerializer, LoginSerializer, MessageSerializer, MessageCreateSerializer
from .serializers import ChatSerializer, ProfileSerializer
from core.serializers import AnnotationSerializer
from rest_framework.permissions import IsAuthenticated

from core.utils import LargeResultsSetPagination, StandardResultsSetPagination

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer




class LoginAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)

        userOb = User.objects.get(username=serializer.validated_data['username'])

        return Response({

                            "id": userOb.id,
                            "first_name": userOb.first_name,
                            "last_name": userOb.last_name,
                            "email" : userOb.email,
                        
                        })

class MessagesAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = MessageSerializer


    # def get(self, request, *args, **kwargs):
    #     author = self.kwargs['pk_sender']
    #     receiver = self.kwargs['pk_receiver']
        
    #     return Response(
    #                         Message.objects.filter(sender=author, receiver=receiver)
    #                 )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sender = request.data['sender']
        receiver = request.data['receiver']
        dict_msg = []; mid_list = [];

        if sender != receiver:
            for pk in Message.objects.filter(sender=sender, receiver=receiver).values():
                dict_msg.append(pk['id'])
                
            for pk in Message.objects.filter(sender=receiver, receiver=sender).values():
                dict_msg.append(pk['id'])
        
        else:
            for pk in Message.objects.filter(sender=sender, receiver=receiver).values():
                dict_msg.append(pk['id'])
        



        # dict_msg dentro da mid_list
        for i in dict_msg:
            mid_list.append( 
                { 
                'id': Message.objects.get(pk=i).id,
                'text': Message.objects.get(pk=i).text,
                'seen': Message.objects.get(pk=i).seen,
                'sender': Message.objects.get(pk=i).sender.id,
                'receiver': Message.objects.get(pk=i).receiver.id,
                'date': Message.objects.get(pk=i).date

                }
            )

        list_definitive = sorted(mid_list, key=lambda k: k['date']) 
        
        
        return Response(
            {"results": list_definitive}
        )

        

class MessagesCreateAPI(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = MessageCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data:


            try:
                sender_ob = User.objects.get(id=request.data['sender'])
                receiver_ob = User.objects.get(id=request.data['receiver'])
                
                
                dict_msg = {
                    "text": request.data["text"]
                }
                
                msg = Message(**dict_msg, sender=sender_ob, receiver=receiver_ob)
                msg.save()
            except Exception as e:
                return Response({"results": e})

            return Response({
                    "results": serializer.validated_data
                })

        else:
            return Response({
                "results": serializer.validated_data
                })


class ChatAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        
        data = [{'id': msg.pk, 'text': msg.text, 'sender': msg.sender.pk, 'date': msg.date} for msg in Message.objects.filter(receiver=request.data['id_user'])]
    
        data = sorted(data, key=lambda k: k['date'], reverse=True) # para pegar o fim da lista de dictionary com as datas mais recentes

        lista_final = []; list_used = []

        for i in range(0, len(data)):
            if i == 0:
                lista_final.append(data[i])
                list_used.append(data[i]['sender'])
            else:
                if data[i-1]['sender'] == data[i]['sender']:
                    continue
                else:
                    if data[i]['sender'] in list_used:
                        continue
                    else:
                        list_used.append(data[i]['sender'])
                        lista_final.append(data[i])
        

        return Response({"results": lista_final})

        


class ProfileAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfileSerializer


    def get_queryset(self):

        target = self.kwargs['pk']
        return Profile.objects.filter(user=target)


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer



class FollowingAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnnotationSerializer
    pagination_class = StandardResultsSetPagination


    def get_queryset(self):
        user_ob = User.objects.get(pk=self.kwargs['pk'])
        profile_ob = Profile.objects.get(user=user_ob)

        lista = []
        for following in profile_ob.following.all():
            lista.append(following)

        return Annotation.objects.filter(author__in=lista, public=True).order_by("-date")
