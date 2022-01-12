from django.urls import include, path
from rest_framework import routers

from .views import (GenreViewSet, TitlesViewSet,
                    CategoryViewSet)

v1 = routers.DefaultRouter()
v1.register('genres', GenreViewSet, basename='genres')
v1.register('titles', TitlesViewSet, basename='titles')
v1.register('categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(v1.urls))
]
