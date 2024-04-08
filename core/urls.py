from django.urls import path
from rest_framework import routers

from .views import UserViewSet, ReferredUserViewSet, CurrentUserAPIView


user_router = routers.DefaultRouter()
user_router.register("users", UserViewSet, basename="user")
user_router.register("users/referred", ReferredUserViewSet, basename="referred_user")

urlpatterns = [
    path("users/me/", CurrentUserAPIView.as_view(), name="current_user"),
]

urlpatterns += user_router.urls
