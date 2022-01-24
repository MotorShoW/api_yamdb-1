from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, TokenViewSet,
                    UserViewSet, get_confirmation_code)

router_v1 = DefaultRouter()
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments',
)
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register(r'users', UserViewSet, basename='users')


auth_url_patterns = [
    path('signup/', get_confirmation_code, name='signup'),
    path('token/', TokenViewSet.as_view(), name='token_obtain_pair'),
]


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_url_patterns)),
]
