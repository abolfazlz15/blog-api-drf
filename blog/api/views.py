from blog.api import serializers
from blog.api.permissions import IsAuthorOrReadOnly
from blog.models import Article
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ArticleListView(APIView):
    def get(self, request):
        instance = Article.objects.filter(status=True)
        serializer = serializers.ArticleListSrializer(instance=instance, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDetailView(APIView):
    def get(self, request, pk):
        instance = Article.objects.get(id=pk)
        serializer = serializers.ArticleDetailSrializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDeleteView(APIView):

    def delete(self, request, pk):
        self.permission_classes = [IsAuthorOrReadOnly]
        article = Article.objects.get(id=pk)
        self.check_object_permissions(request, article)

        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ArticleAddView(APIView):
    def post(self, request):
        serializer = serializers.ArticleAddSrializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'result': 'article added'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ArticleUpdateView(APIView):
    def put(self, request, pk):
        self.permission_classes = [IsAuthorOrReadOnly]
        instance = Article.objects.get(id=pk)
        self.check_object_permissions(request, instance)
        serializer = serializers.ArticleAddSrializer(instance=instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'result': 'article updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
