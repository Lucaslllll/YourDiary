from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Category, Annotation, Comment, Report, Favorite



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = '__all__'


class AnnotationAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ["author"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class FavoriteCheckSerializer(serializers.Serializer):
    id = serializers.CharField(allow_blank=True, allow_null=True)
    user = serializers.IntegerField()
    annotation = serializers.IntegerField()

    def validate(self, data):

        try:
            favoriteOb = Favorite.objects.get(user=data['user'], annotation=data['annotation'])
        except Favorite.DoesNotExist:
            raise serializers.ValidationError(False)

        data['id'] = favoriteOb.id
        return data


