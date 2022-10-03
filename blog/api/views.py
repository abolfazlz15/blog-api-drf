from blog.api import serializers
from blog.api.permissions import IsAuthorOrReadOnly, IsAuthor
from blog.models import Article
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import filters


class ArticleListView(ListAPIView):
    queryset = Article.objects.filter(status=True)
    serializer_class = serializers.ArticleListSrializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'text']
    filterset_fields = ['category', 'author', 'tag']


# class ArticleListView(APIView):
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['category']
#     def get(self, request):
#         instance = Article.objects.filter(status=True)
#         serializer = serializers.ArticleListSrializer(instance=instance, many=True)
#         filter_backends = [DjangoFilterBackend]
#         filterset_fields = ['category']
#         return Response(serializer.data, status=status.HTTP_200_OK)


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
    permission_classes = [IsAuthor]
    def post(self, request):
        serializer = serializers.ArticleAddSrializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'result': 'article added'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ArticleUpdateView(APIView):
    permission_classes = [IsAuthorOrReadOnly]

    def put(self, request, pk):
        
        instance = Article.objects.get(id=pk)
        self.check_object_permissions(request, instance)
        if request.user.is_admin or request.user.is_superuser:
            serializer = serializers.ArticleAddAdminSrializer(instance=instance, data=request.data, partial=True)
        else:
            serializer = serializers.ArticleAddAuthorSrializer(instance=instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'result': 'article updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryAddView(APIView):
    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'result': 'category added'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)