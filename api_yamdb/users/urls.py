from django.urls import path

from .views import SignUpAPIView, TokenAPIView

urlpatterns = [
    path('signup/', SignUpAPIView.as_view(), name='signup'),
    path('token/', TokenAPIView.as_view(), name='token')
]
