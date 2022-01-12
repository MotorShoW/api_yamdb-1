from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (GenreViewSet, TitlesViewSet,
                    CategoryViewSet, UserViewSet,
                    SignUpVeiwSet, TokenViewSet)

router = DefaultRouter()
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitlesViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register(r'users', UserViewSet)


auth_url_patterns = [
    path('signup/', SignUpVeiwSet.as_view()),
    path('token/', TokenViewSet.as_view(), name='token_obtain_pair'),
]


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_url_patterns)),
    path('v1/', include(router.urls)),

]
