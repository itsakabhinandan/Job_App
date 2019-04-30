from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model

class intro(models.Model):
    name = models.CharField(max_length=30, default="")
    email = models.CharField(max_length=30, default="")
    message = models.CharField(max_length=30, default="")

    def __str__(self):
        return self.name


class Signup(models.Model):
    first_name = models.CharField(max_length=10, default="")
    last_name = models.CharField(max_length=10, default="")
    email = models.CharField(max_length=10, default="")
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=10)
    cpassword = models.CharField(max_length=10)

    def __str__(self):
        return self.username


class Signuprec(models.Model):

    first_name = models.CharField(max_length=10, default="")
    last_name = models.CharField(max_length=10, default="")
    designation = models.CharField(max_length=15, default="")
    email = models.CharField(max_length=20, default="")
    company = models.CharField(max_length=20, default="")
    office_ad = models.CharField(max_length=20, default="")
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=10)
    cpassword = models.CharField(max_length=10)

    def __str__(self):
        return self.username

class Profile(models.Model):

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE
    )
    designation = models.CharField(max_length=100, null=True)
    company = models.CharField(max_length=100, null=True)
    office_address = models.CharField(max_length=100, null=True)

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Resume(models.Model):

    resume = models.FileField(upload_to='resume/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Job(models.Model):

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    category = models.CharField(max_length=100, null=True)
    experience = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=100, null=True)
    qualification = models.CharField(max_length=100, null=True)

    deleted = models.BooleanField(default=False)

    deadline = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class JobApplication(models.Model):

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    job = models.ForeignKey(
        Job,
        null=True,
        on_delete=models.SET_NULL
    )
    resume = models.ForeignKey(
        Resume,
        null=True,
        on_delete=models.SET_NULL
    )
    sites = models.CharField(max_length=1024)
    email = models.EmailField()
    skills = models.CharField(max_length=1024)
    score = models.FloatField()
    video_token = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)