from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Message, Profile



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_password(self, data):
        value = make_password(password=data, salt=None, hasher='pbkdf2_sha256')
        return value

    def validate_terms_of_use(self, data):
        if not data:
            raise serializers.ValidationError("terms of use not marked")
        return data

    

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


class MessageSerializer(serializers.Serializer):
    sender = serializers.CharField()
    receiver = serializers.CharField()


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ChatSerializer(serializers.Serializer):
    id_user = serializers.CharField()
    
    def validate(self, data):
        pk = data['id_user']
        
        try:
            userOb = User.objects.get(id=int(pk))
        except User.DoesNotExist:
            raise serializers.ValidationError("Dados errados")

        # mandar logo um true nessa validate data
        return True

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'



class GetUserSerializer(serializers.Serializer):
    token = serializers.CharField()



class SendEmailSerializer(serializers.Serializer):
    id = serializers.CharField()
    email = serializers.CharField()



class RedefineSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, data):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, data['email']):
            return data
        else:
            raise serializers.ValidationError("Email is Invalid")

class ConfirmeSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    confirme_password = serializers.CharField()

    def validate(self, data):
        password1 = data['password']
        password2 = data['confirme_password']

        if password1 == password2:
            try:
                userOb = User.objects.get(username=data['username'])
            except User.DoesNotExist:
                raise serializers.ValidationError("User Does Not Exist")

            return data

        else:
            raise serializers.ValidationError("Passwords not match")