from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.hashers import make_password, check_password

from .models import User, Message, Profile
from core.models import Annotation
from .serializers import UserSerializer, LoginSerializer, MessageSerializer, MessageCreateSerializer
from .serializers import ChatSerializer, ProfileSerializer, RedefineSerializer, ConfirmeSerializer
from .serializers import SendEmailSerializer
from .utils import CodeProcessing
from core.serializers import AnnotationSerializer
from rest_framework.permissions import IsAuthenticated

from core.utils import LargeResultsSetPagination, StandardResultsSetPagination
from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string



class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post', 'patch', 'get', 'head']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # sobreescrever para as infos cadastradas não retornem
        return Response({}, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        new_data = serializer.data
        del new_data["password"]
        # del new_data["email"]
        return Response(new_data)


class LoginAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        userOb = User.objects.get(username=serializer.validated_data['username'])

        return Response({

                            "id": userOb.id,
                            "first_name": userOb.first_name,
                            "last_name": userOb.last_name,
                            "email" : userOb.email,
                        
                        })




class SendEmailAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = SendEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = SendEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(pk=serializer.data['id'])  
        except User.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


        user.email = serializer.data['email']
        user.save()


        return Response({}, status=status.HTTP_200_OK)



class RedefinePasswordAPI(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = RedefineSerializer

    def post(self, request, *args, **kwargs):
        serializer = RedefineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.data['email'])  
        except User.DoesNotExist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        token = CodeProcessing(user.username)
        token = token.create()

        if token == False:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        elif token == None:
            return Response({"error": "email already send, wait 15 minutes"}, status=status.HTTP_400_BAD_REQUEST)

        msg_html = render_to_string('email.html', 
            {
                'token':token
            }
        )
        connection = mail.get_connection()
        connection.open()

        email = mail.EmailMessage(
            'Suporte - YourDiary',
            msg_html,   
            'yourdiary.oficial@gmail.com', # 'from'
            [user.email,], # 'to'
            connection=connection
        )

        email.send()

        return Response({}, status=status.HTTP_200_OK)


class ConfirmePasswordAPI(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated, )
    serializer_class = ConfirmeSerializer

    def put(self, request, *args, **kwargs):
        serializer = ConfirmeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = CodeProcessing(serializer.data['username'])
        token = token.verify(kwargs['token'])
            
        if not token:
            return Response({"error": "token is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        elif token == None:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(username=serializer.data['username'])
        
        user.password = make_password(password=serializer.data['password'], salt=None, hasher='pbkdf2_sha256')
        user.save()

        return Response({}, status=status.HTTP_200_OK)


class MessagesAPI(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated, )
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


