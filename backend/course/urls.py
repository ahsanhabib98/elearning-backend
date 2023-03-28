from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    CourseViewSet,
    ModuleViewSet,
    LectureViewSet,
    ForumViewSet,
    LiveClassViewSet,
    VideoWatchedViewSet,
    CourseEnrollView
)

router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'module', ModuleViewSet)
router.register(r'lecture', LectureViewSet)
router.register(r'live-class', LiveClassViewSet)
router.register(r'forum', ForumViewSet)
router.register(r'video-watched', VideoWatchedViewSet)
router.register(r'', CourseViewSet)
urlpatterns = [
    path("course-enroll/", CourseEnrollView.as_view(), name="course_enroll"),
] + router.urls