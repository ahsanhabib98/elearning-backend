from django.urls import path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView
)

from .views import (
    UserRegisterView,
    UserLoginView,
    ChangePasswordView,
    UserViewSet, 
    InstructorViewSet, 
    LearnerViewSet,
    CurrentLoggedInUser,
    VerifyEmail
)

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'instructor', InstructorViewSet)
router.register(r'learner', LearnerViewSet)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("registration/", UserRegisterView.as_view(), name="register"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path("password-change/<int:pk>/",ChangePasswordView.as_view(), name="password_change"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path('user/', CurrentLoggedInUser.as_view({'get': 'retrieve'}), name="current_user"),

] + router.urls

