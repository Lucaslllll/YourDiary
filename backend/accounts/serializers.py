from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_password(self, data):
        value = make_password(password=data, salt=None, hasher='pbkdf2_sha256')
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


    def validate(self, data):
        

        try:
            userOb = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            userOb = None

        if userOb == None:
            raise serializers.ValidationError("Dados errados, 01")

        corresponde = check_password(password=data['password'], encoded=userOb.password)


        if corresponde == False:
            raise serializers.ValidationError("Dados errados, 02")


        return data