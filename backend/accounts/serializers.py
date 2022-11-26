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