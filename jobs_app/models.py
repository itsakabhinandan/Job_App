from django.db import models

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

class Resume(models.Model):

    resume = models.FileField(upload_to='resume/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
