from rest_framework import serializers

from apps.common.models import *


class BookSerializers(serializers.Serializer):
    class Meta:
        model = Book
        fields = ['title', 'description', 'pdf', 'rating', 'category']


class MyFavoriteBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyFavoriteBook
        fields = ['user', 'book']
       