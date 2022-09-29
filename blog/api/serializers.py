from rest_framework import serializers
from blog.models import Article



class ArticleListSrializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    category = serializers.SlugRelatedField(read_only=True, slug_field='title')
    class Meta:
        model = Article
        fields = ('title', 'image', 'author', 'category')


class ArticleDetailSrializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='title')
    tag = serializers.SlugRelatedField(read_only=True, slug_field='title')
    author = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Article
        exclude = ('status', 'updated_at')


class ArticleAddSrializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Article
        exclude = ('status', 'updated_at')
