from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.hashers import make_password, check_password

from .models import User, Message
from .serializers import UserSerializer, LoginSerializer, MessageSerializer, MessageCreateSerializer
from .serializers import ChatSerializer
from rest_framework.permissions import IsAuthenticated


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
    #permission_classes = (IsAuthenticated, )
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

        if serializer.validated_data:
            sender = request.data['sender']
            receiver = request.data['receiver']

            dict_msg = {}; n = 0;

            if sender != receiver:
                for pk in Message.objects.filter(sender=sender, receiver=receiver).values():
                    dict_msg[n] = pk['id']
                    n += 1
                for pk in Message.objects.filter(sender=receiver, receiver=sender).values():
                    dict_msg[n] = pk['id']
                    n += 1
            else:
                for pk in Message.objects.filter(sender=sender, receiver=receiver).values():
                    dict_msg[n] = pk['id']
                    n += 1


            lista = [None]*len(dict_msg); n = 0

            # dict_msg dentro da lista
            for i in dict_msg.values():
                lista[n] = { 
                    'id': Message.objects.get(pk=i).id,
                    'text': Message.objects.get(pk=i).text,
                    'seen': Message.objects.get(pk=i).seen,
                    'sender': Message.objects.get(pk=i).sender.id,
                    'receiver': Message.objects.get(pk=i).receiver.id,
                    'date': Message.objects.get(pk=i).date

                }
                n += 1

            list_definitive = sorted(lista, key=lambda k: k['date']) 
            # dic_definitives = {}; contador = 0
            # for dic in lista:
            #     dic_definitives[contador] = dic
            #     contador += 1
            # print(dic_definitives)
            # ordenado = sorted(dic_definitives, key=lambda dic_definitive: dic_definitives[dic_definitive]['date'])
            # print(dic_definitives)
            return Response(
                {"results": list_definitive}
            )

        else:
            return Response(
                {"results": serializer.validated_data}
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

        if serializer.validated_data:

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

        else:
            return Response({"results": "source"}, status.HTTP_400_BAD_REQUEST)
