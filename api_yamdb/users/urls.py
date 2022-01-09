from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignUpVeiwSet, TokenViewSet, UserViewSet

router = DefaultRouter()


router.register(r'users', UserViewSet)

auth_url_patterns = [
    path('signup/', SignUpVeiwSet.as_view()),
    path('token/', TokenViewSet.as_view(), name='token_obtain_pair'),
]

urlpatterns = [
    path('v1/auth/', include(auth_url_patterns)),
    path('v1/', include(router.urls)),
]
