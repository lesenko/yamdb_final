from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import AdminViewSet, UserAPIView

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='Reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='Comments'
)
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'users', AdminViewSet, basename='users')


urlpatterns = [
    path('v1/auth/', include('users.urls')),
    path('v1/users/me/', UserAPIView.as_view(), name='me'),
    path('v1/', include(router.urls)),
]
