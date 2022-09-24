from blog.models import Article
from rest_framework.views import APIView
from blog.api.serializers import ArticleListSrializer
from rest_framework.response import Response


class ArticleListView(APIView):
    def get(self, request):
        instance = Article.objects.filter(status=True)
        serializer = ArticleListSrializer(instance=instance, many=True)

        return Response(serializer.data)
