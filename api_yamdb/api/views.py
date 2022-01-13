import uuid

from django.core import exceptions
from django.core.mail import send_mail
from rest_framework import viewsets, filters, status, exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .models.models import Titles, Genre, Category, User
from .serializers import (TitleCreateSerializer, TitlesSerializer,
                          GenreSerializer, CategorySerializer,
                          SignUpSerializer, TokenSerializer, UserSerializer)
from .permissions import IsAdmin, ReadOnly


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug',
        url_name='category_slug'
    )
    def get_genre(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    @action(
        detail=False, methods=['delete'],
        url_path=r'(?P<slug>\w+)',
        lookup_field='slug',
        url_name='category_slug'
    )
    def get_category(self, request, slug):
        category = self.get_object()
        serializer = CategorySerializer(category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAdmin | ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateSerializer
        return TitlesSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin)
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]

    @action(
        detail=False,
        methods=('get', 'patch', 'post'),
        permission_classes=(IsAuthenticated,),
        url_path='me', url_name='me'
    )
    def me(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(email=instance.email, role=instance.role)
        return Response(serializer.data)


class TokenViewSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        serializer = TokenSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(
                email=serializer.data['email'],
                confirmation_code=serializer.data['confirmation_code']
            )
        except exceptions.ValidationError:
            return Response(
                data={'detail': 'Invalid email or code'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            user.is_active = True
            user.save()
            refresh_token = RefreshToken.for_user(user)
            return Response({'token': str(refresh_token.access_token)})


class SignUpVeiwSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            if email is None:
                return Response(request.data, status.HTTP_400_BAD_REQUEST)
            confirmation_code = uuid.uuid4()
            User.objects.create(
                email=email, username=str(email),
                confirmation_code=confirmation_code, is_active=False
            )
            send_mail(
                'Account verification',
                'Your activation key {}'.format(confirmation_code),
                DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            return Response(
                {'result': 'A confirmation code has been sent to your email'},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
