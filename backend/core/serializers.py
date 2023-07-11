from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import Category, Annotation, Comment, Report, Favorite, Like
from .models import AnnotationImage



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = '__all__'




class AnnotationCryptSerializer(serializers.ModelSerializer):
    annotation = AnnotationSerializer()
    key = serializers.CharField(required=True)
    class Meta:
        model = Annotation
        fields = ['annotation', 'key']

    def validate(self, data):

        if data['key'] == True:
            key = data['key']
            key = key.encode()
            # bytes encriptados
            data['annotation']['text'] = encrypt_c.encrypt_text(key, bytes(data['annotation']['text']))

        return data

class AnnotationAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ["author"]

class AnnotationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnotationImage
        fields = '__all__'


class SearchSerializer(serializers.Serializer):
    text = serializers.CharField()


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


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class LikeCheckSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    user = serializers.IntegerField()
    annotation = serializers.IntegerField()

    def validate(self, data):

        try:
            likeOb = Like.objects.get(user=data['user'], annotation=data['annotation'])
        except Like.DoesNotExist:
            raise serializers.ValidationError(False)

        data['id'] = likeOb.id
        return data
