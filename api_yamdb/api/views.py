from rest_framework import viewsets, filters
from models.models import Titles, Genre, Category
from .serializers import (TitlesSerializer, GenreSerializer,
                          CategorySerializer)
from .permissions import IsAdmin, ReadOnly


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin, ReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin, ReadOnly]
    filter_backends = (filters.SearchFilter,)
    serach_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [IsAdmin, ReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
