from blog.api.serializers import ArticleListSrializer, ArticleDetailSrializer
from blog.models import Article
from rest_framework.response import Response
from rest_framework.views import APIView


class ArticleListView(APIView):
    def get(self, request):
        instance = Article.objects.filter(status=True)
        serializer = ArticleListSrializer(instance=instance, many=True)

        return Response(serializer.data)

class ArticleDetailView(APIView):
    def get(self, request, pk):
        instance = Article.objects.get(id=pk)
        serializer = ArticleDetailSrializer(instance=instance)
        return Response(serializer.data)