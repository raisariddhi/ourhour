from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.timezone import now



class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='instructor')

class Course(models.Model):
    course_id = models.CharField(max_length=7, primary_key=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    instructors = models.ManyToManyField(Instructor)

class Ticket(models.Model):
    status_options = (
        (1, "waiting"),
        (2, "active"),
        (3, "complete"),
        (4, "cancelled")
    )
    length_options = (
        (1, "short"),
        (2, "medium"),
        (3, "long")
    )
    phone_regex = RegexValidator(regex=r'^\+?[1-9]\d{,14}$',
            message="Phone number must be in E.164 format"
            )

    ticket_id = models.AutoField(primary_key=True)
    desc = models.CharField(max_length=256)
    phone = models.CharField(validators=[phone_regex], max_length=15)
    creation_time = models.DateTimeField(default=now)
    finish_time = models.DateTimeField(auto_now=False, null=True, blank=True)
    status = models.IntegerField(choices=status_options, default=1)
    length = models.IntegerField(choices=length_options, default=1)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    
