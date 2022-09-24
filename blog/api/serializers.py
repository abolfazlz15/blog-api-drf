from rest_framework import serializers
from blog.models import Article



class ArticleListSrializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    class Meta:
        model = Article
        fields = ('title', 'image', 'author', 'category')

