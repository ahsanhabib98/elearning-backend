from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import (
    Category,
    Course,
    Module,
    Lecture,
    Forum,
    LiveClass,
    VideoWatched
)
from .serializers import (
    CategorySerializer,
    CourseSerializer,
    ModuleSerializer,
    LectureSerializer,
    ForumSerializer,
    LiveClassSerializer,
    VideoWatchedSerializer
)
from .permissions import (
    IsCourseOwnerOrReadOnly,
    IsModuleOwnerOrReadOnly,
    IsLectureOwnerOrReadOnly,
    IsForumOwnerOrReadOnly,
    IsLiveClassOwnerOrReadOnly,
    IsVideoWatchedOwnerOrReadOnly
)
from user.models import Instructor, Learner

# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(parent=None)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsCourseOwnerOrReadOnly]

    def perform_create(self, serializer):
        instructor = Instructor.objects.get(user=self.request.user)
        serializer.save(instructor=instructor)


class CourseEnrollView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        course = request.data.get("course", None)
        if course is None:
            return Response({"message": "Required learner and course."}, status=HTTP_400_BAD_REQUEST)
        course = get_object_or_404(Course, id=course)
        learner = request.user.learner
        course.learners.add(learner)
        course.save()
        return Response({"message": "Successfully course enrolled."}, status=HTTP_200_OK)


class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsModuleOwnerOrReadOnly]


class LectureViewSet(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    permission_classes = [IsLectureOwnerOrReadOnly]


class VideoWatchedViewSet(viewsets.ModelViewSet):
    serializer_class = VideoWatchedSerializer
    queryset = VideoWatched.objects.all()
    permission_classes = [IsVideoWatchedOwnerOrReadOnly]

    def perform_create(self, serializer):
        learner = get_object_or_404(Learner, user=self.request.user)
        serializer.save(learner=learner)


class ForumViewSet(viewsets.ModelViewSet):
    serializer_class = ForumSerializer
    queryset = Forum.objects.filter(parent=None)
    permission_classes = [IsForumOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LiveClassViewSet(viewsets.ModelViewSet):
    serializer_class = LiveClassSerializer
    queryset = LiveClass.objects.all()
    permission_classes = [IsLiveClassOwnerOrReadOnly]
