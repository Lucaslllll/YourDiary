from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
