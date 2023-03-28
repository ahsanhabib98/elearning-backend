from django.db import models
from django.shortcuts import get_object_or_404
from user.models import Instructor, Learner, User
from utils.requestutils import get_current_request

# Create your models here.


class Category(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


COURSE_LEVEL_CHOICES = (
        ('Beginner','Beginner'),
        ('Intermediate','Intermediate'),
        ('Advance','Advance'),
    )


class Course(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=200)
    preview_video = models.TextField()
    cover_image = models.ImageField(upload_to='course/cover_image', blank=True, null=True)
    description = models.TextField()
    requirement = models.TextField()
    course_outcome = models.TextField()
    resource_file = models.FileField(upload_to='course/resource_file', blank=True, null=True)
    optional_reading = models.TextField(null=True, blank=True)
    module_detail = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    sale_price = models.IntegerField()
    level = models.CharField(max_length=20, choices=COURSE_LEVEL_CHOICES)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='instructor_courses')
    learners = models.ManyToManyField(Learner, blank=True, related_name='learner_courses')
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categorywise_courses')

    def __str__(self):
        return self.title

    def get_course_duration(self):
        totalSecs = 0
        for module in self.course_modules.all():
            timeParts = [int(s) for s in module.get_module_duration().split(':')]
            totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
        totalSecs, sec = divmod(totalSecs, 60)
        hr, min = divmod(totalSecs, 60)
        return "%d:%02d:%02d" % (hr, min, sec)

    def get_course_lecture_count(self):
        result = 0
        for module in self.course_modules.all():
           result += module.get_module_lecture_count()
        return result

    def get_user_course_video_wataches_count(self):
        try:
            total_count = 0
            for module in self.course_modules.all():
                total_count += module.get_user_module_video_wataches_count()
            return total_count
        except:
            return None


class Rating(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='learner_ratings')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_ratings')
    rating = models.IntegerField()
    review = models.TextField()

    def __str__(self):
        return self.learner.name


class Module(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_modules')
    exercise_file = models.FileField(upload_to='course/module/exercise_file', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_module_duration(self):
        totalSecs = 0
        for lecture in self.lectures.all():
            timeParts = [int(s) for s in str(lecture.video_length).split(':')]
            totalSecs += (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
        totalSecs, sec = divmod(totalSecs, 60)
        hr, min = divmod(totalSecs, 60)
        return "%d:%02d:%02d" % (hr, min, sec)

    def get_module_lecture_count(self):
        return self.lectures.all().count()

    def get_user_module_video_wataches_count(self):
        try:
            total_count = 0
            for lecture in self.lectures.all():
                total_count += lecture.get_user_lecture_video_wataches_count()
            return total_count
        except:
            return None


class Lecture(models.Model):
    video = models.FileField(upload_to='course/lecture_video')
    title = models.CharField(max_length=100)
    video_length = models.TimeField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lectures')

    def __str__(self):
        return self.title

    def get_user_lecture_video_wataches_count(self):
        try:
            request = get_current_request()
            if request.user.is_authenticated:
                learner = get_object_or_404(Learner, user=request.user)
                for video_watch in self.video_watches.all():
                    if video_watch.learner == learner:
                        return 1
                return 0
            return None
        except:
            return None


class VideoWatched(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='video_watches')
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='video_watches')
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.learner.name


class Forum(models.Model):
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_forums')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_forums')

    def __str__(self):
        return self.question


class LiveClass(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='classes')
    modules = models.ManyToManyField(Module, blank=True, related_name='classes')
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    session_date = models.DateField()
    session_time = models.TimeField()
    video = models.FileField(upload_to='course/live_class')
    resource_file = models.FileField(upload_to='course/live_class/resource_file', blank=True, null=True)

    def __str__(self):
        return self.course.title