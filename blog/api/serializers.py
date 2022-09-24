from rest_framework import serializers
from blog.models import Article



class ArticleListSrializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'image', 'author', 'category')

