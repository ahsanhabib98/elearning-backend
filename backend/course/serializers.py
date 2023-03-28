from django.shortcuts import get_object_or_404

from rest_framework import serializers

from user.serializers import (
    InstructorSerializer,
    UserSerializer
)

from user.models import Learner
from .models import (
    Category,
    Course,
    Module,
    Lecture,
    Forum,
    LiveClass,
    VideoWatched
)


class ChildCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    childs = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'childs']

    def get_childs(self, obj):
        return ChildCategorySerializer(Category.objects.filter(parent=obj), many=True).data


class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.SerializerMethodField()
    modules = serializers.SerializerMethodField()
    forums = serializers.SerializerMethodField()
    classes = serializers.SerializerMethodField()
    course_enroll = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    lecture_count = serializers.SerializerMethodField()
    user_video_watches_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('instructor', 'learners', 'modules')

    def get_instructor(self, obj):
        return InstructorSerializer(obj.instructor).data

    def get_modules(self, obj):
        try:
            request = self.context.get('request', None)
            if request.user.is_authenticated:
                return ModuleSerializer(obj.course_modules.all(), many=True, context={'request': request}).data
            return None
        except:
            return None

    def get_forums(self, obj):
        return ForumSerializer(obj.course_forums.all(), many=True).data

    def get_classes(self, obj):
        try:
            request = self.context.get('request', None)
            if request.user.is_authenticated:
                return LiveClassSerializer(obj.classes.all(), many=True).data
            return None
        except:
            return None

    def get_course_enroll(self, obj):
        try:
            request = self.context.get('request', None)
            if request.user.is_authenticated:
                learner = get_object_or_404(Learner, user=request.user)
                if learner in obj.learners.all():
                    return True
                return False
            return None
        except:
            return None

    def get_duration(self, obj):
        return obj.get_course_duration()
    
    def get_lecture_count(self, obj):
        return obj.get_course_lecture_count()

    def get_user_video_watches_count(self, obj):
        return obj.get_user_course_video_wataches_count()


class ModuleSerializer(serializers.ModelSerializer):
    lectures = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    lecture_count = serializers.SerializerMethodField()
    user_video_watches_count = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = '__all__'
        read_only_fields = ('lectures', 'classes', 'duration')

    def get_lectures(self, obj):
        try:
            request = self.context.get('request', None)
            return LectureSerializer(obj.lectures.all(), many=True, context={'request': request}).data
        except:
            return LectureSerializer(obj.lectures.all(), many=True).data

    def get_duration(self, obj):
        return obj.get_module_duration()

    def get_lecture_count(self, obj):
        return obj.get_module_lecture_count()

    def get_user_video_watches_count(self, obj):
        return obj.get_user_module_video_wataches_count()


class LectureSerializer(serializers.ModelSerializer):
    video_watches = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = '__all__'
        read_only_fields = ('learner', 'video_watches' )

    def get_video_watches(self, obj):
        try:
            request = self.context.get('request', None)
            if request.user.is_authenticated:
                learner = get_object_or_404(Learner, user=request.user)
                for video_watch in obj.video_watches.all():
                    if video_watch.learner == learner:
                        return True
                return False
            return None
        except:
            return None


class VideoWatchedSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoWatched
        fields = '__all__'
        read_only_fields = ('learner', )


class ReplyForumSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Forum
        fields = '__all__'
        read_only_fields = ('user', )

    def get_user(self, obj):
        return UserSerializer(obj.user).data


class ForumSerializer(serializers.ModelSerializer):
    replys = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Forum
        fields = '__all__'
        read_only_fields = ('replys', 'user')

    def get_replys(self, obj):
        return ReplyForumSerializer(Forum.objects.filter(parent=obj), many=True).data

    def get_user(self, obj):
        return UserSerializer(obj.user).data


class LiveClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClass
        fields = '__all__'