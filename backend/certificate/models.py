from django.db import models
from user.models import Learner
from course.models import Course

# Create your models here.


class Certificate(models.Model):
    validation_code = models.CharField(max_length=30)
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='learner_certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_certificates')
    completion_date = models.DateField()
    expire_date = models.DateField()

    def __str__(self):
        return self.validation_code