from rest_framework import serializers
from blog.models import Article, Category, Tag



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




class ArticleAddAuthorSrializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.BooleanField(read_only=True)
    author = serializers.IntegerField(read_only=True)
    class Meta:
        model = Article
        exclude = ('updated_at',)


class ArticleAddAdminSrializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Article
        exclude = ('updated_at',)        


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)

    def validate_title(self, value):
        object =  Category.objects.filter(title=value)

        if object:
            raise serializers.ValidationError({'error': 'this category exist'})
        else:    
            return value