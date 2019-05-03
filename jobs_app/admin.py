from django.contrib import admin
from jobs_app.models import intro, Signup, Signuprec
from jobs_app.models import Job, JobApplication

# Register your models here.

admin.site.register(intro)
admin.site.register(Signup)
admin.site.register(Signuprec)
admin.site.register(JobApplication)
admin.site.register(Job)