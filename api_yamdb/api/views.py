from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from reviews.models import Category, Genre, Review, Title

from api.filters import TitleFilter
from api.permissions import IsOwnerOrModeratorOrAdminOrReadOnly
from api.serializers import CommentSerializer, ReviewSerializer

from .permissions import AdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          TitleSerializerCreate)


class ListCreateDestroyMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(ListCreateDestroyMixin):
    permission_classes = [AdminOrReadOnly]
    pagination_class = PageNumberPagination
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyMixin):
    permission_classes = [AdminOrReadOnly]
    pagination_class = PageNumberPagination
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOrReadOnly]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializerCreate
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsOwnerOrModeratorOrAdminOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        text = self.request.data.get('text')
        score = self.request.data.get('score')
        serializer.save(
            text=text,
            author=self.request.user,
            title=title,
            score=score
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsOwnerOrModeratorOrAdminOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        text = self.request.data.get('text')
        serializer.save(
            text=text,
            author=self.request.user,
            review=review
        )
