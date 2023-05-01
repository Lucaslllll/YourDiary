from .models import Code
import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, mixins, serializers
from django.db import IntegrityError



class CodeProcessing(object):

    def __init__(self, username):
        self.username = username

    def create(self):
        token = jwt.encode({"username": self.username}, key=settings.SECRET_KEY, algorithm="HS256")
        dict_code = {"value": token}
        
        try:    
            code = Code(**dict_code)
            code.save()
            return code.value
        except IntegrityError:
            return None
        except:
            return False


    def verify(self, token):
        payload=jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])

        if self.username == payload['username']:
            try:
                code = Code.objects.get(value=token)
            except:
                return False

            return True

        else:
            return None