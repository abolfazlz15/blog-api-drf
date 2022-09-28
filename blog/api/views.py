from blog.api.serializers import ArticleListSrializer, ArticleDetailSrializer
from blog.models import Article
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class ArticleListView(APIView):
    def get(self, request):
        instance = Article.objects.filter(status=True)
        serializer = ArticleListSrializer(instance=instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDetailView(APIView):
    def get(self, request, pk):
        instance = Article.objects.get(id=pk)
        serializer = ArticleDetailSrializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDeleteView(APIView):
    def delete(self, request, pk):
        article = Article.objects.get(id=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
