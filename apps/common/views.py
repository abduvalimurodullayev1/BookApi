import redis
from rest_framework import generics
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.common.models import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
import django_filters
from django.http import FileResponse
from rest_framework.viewsets import ModelViewSet
# Configure Redis connection
from apps.common.permissions import IsAuthor
from apps.serializers import BookSerializers, MyFavoriteBookSerializer

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)

from rest_framework.views import APIView


@api_view(["GET"])
def health_check_redis(request):
    try:
        # Check Redis connection
        redis_client.ping()
        return Response({"status": "success"}, status=status.HTTP_200_OK)
    except redis.ConnectionError:
        return Response(
            {"status": "error", "message": "Redis server is not working."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class BookList(generics.ListAPIView):
    serializer_class = BookSerializers
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


class BookCreate(generics.CreateAPIView):
    serializer_class = BookSerializers
    queryset = Book.objects.all()
    permission_classes = [IsAdminUser]


class BookDelete(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class BookUpdate(generics.UpdateAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = "pk"
    serializer_class = BookSerializers


class BookDownload(APIView):
    def get(self, pk, request):
        try:
            book = Book.objects.get(pk=pk)
            if book.pdf:
                response = FileResponse(book.pdf.open("rb"), as_attachment=True, filename=book.pdf.name)
                return response
            else:
                return Response("Kitob mavjud emas", status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist:
            return Response({"error": "Kitob topilmadi"})


class MyFavoriteBook(ModelViewSet):
    queryset = MyFavoriteBook.objects.all()
    serializer_class = MyFavoriteBookSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
    serializer_class = BookSerializers


