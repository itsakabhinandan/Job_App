from django.views import View
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404

from jobs_app.forms import ResumeForm, RecruiterCreationForm, JobForm
from jobs_app.models import Job

from jobs_app.forms import SignupForm, Signupformrec, LoginForm
from jobs_app.models import intro, Signup, Signuprec

from jobs_app.utils import parse_resume


class UserSignUpView(View):

    def get(self, request):
        return render(request, 'sign_can/sign_can.html')
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('can_dash')
        return render(request, 'sign_can/sign_can.html', {
            'form': form,
        })

class RecruiterSignUpView(View):

    def get(self, request):
        return render(request, 'sign_rec/sign_rec.html')

    def post(self, request):
        form = RecruiterCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            group = Group.objects.get(name='recruiter')
            group.user_set.add(user)
            user.profile.designation = form.cleaned_data.get('designation')
            user.profile.company = form.cleaned_data.get('company')
            user.profile.office_address = form.cleaned_data.get('company_address')
            user.save()
            password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=password)
            auth_login(request, user)
            return redirect('dash')
        return render(request, 'sign_rec/sign_rec.html', {
            'form': form,
        })

class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated():
            if request.user.has_perm("can_access_recruiter_dashboard"):
                return redirect("dash")
            return redirect("can_dash")
        return render(request, 'login/login.html')
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.has_perm('can_access_recruiter_dashboard'):
                    return redirect('dash')
                return redirect('can_dash')
            else:
                return render(request, 'login/login.html', {
                    'form': form,
                    'error': 'Username or password incorrect'
                })
        return render(request, 'login/login.html', {
            'form': form,
        })

class LogoutView(View):

    def get(self, request):
        if request.user.is_authenticated():
            auth_logout(request)
        return redirect('home')


class JobCreationView(PermissionRequiredMixin, View):

    permission_required = ("can_create_job", )

    def get(self, request):
        return render(request, 'dash_emp/create_job.html')
    
    def post(self, request):
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            return render(request, 'dash_emp/create_job.html')
        return render(request, 'dash_emp/create_job.html', {
            'form': form,
        })

class JobDetailView(View):

    def get(self, request, job_id):
        instance = get_object_or_404(Job, id=job_id)
        return render(request, 'job_detail.html', {
            'job': instance
        })

class JobUpdateView(PermissionRequiredMixin, View):

    permission_required = ("can_create_job", )

    def get(self, request, job_id):
        instance = get_object_or_404(Job, id=job_id)
        form = JobForm(instance=instance)
        return render(request, 'dash_emp/update_job.html', {
            'form': form,
        })

    def post(self, request, job_id):
        instance = get_object_or_404(Job, id=job_id)
        form = JobForm(request.POST)
        if form.is_valid():
            instance.title = form.cleaned_data.get('title')
            instance.description = form.cleaned_data.get('description')
            instance.category = form.cleaned_data.get('category')
            instance.type = form.cleaned_data.get('type')
            instance.qualification = form.cleaned_data.get('qualification')
            instance.experience = form.cleaned_data.get('experience')
            instance.deadline = form.cleaned_data.get('deadline')
            instance.save()
            return redirect('job-detail', job_id=job_id)
        return render(request, 'dash_emp/update_job.html', {
            'form': form,
        })


class RecruiterManageJobsView(PermissionRequiredMixin, View):

    permission_required = ("can_post_job", )

    def get(self, request):
        jobs = request.user.job_set.all()
        print(jobs)
        for job in jobs:
            print(job.jobapplication_set.count())
        return render(request, 'dash_emp/manage_jobs.html', {
            'jobs': jobs
        })


def home(request):
    if request.method == 'POST':
        n = request.POST['name']
        r = request.POST['email']
        a = request.POST['message']

        s = intro()
        s.name = n
        s.email = a
        s.message = r
        s.save()
        return render(request, 'login/login.html')
    else:

        return render(request, 'jobs_app/index.html')

def menu_emp(request):
    return render(request, "menu_emp/menu_emp.html")


def menu_can(request):
    return render(request, "menu_can/menu_can.html")


def dash_emp(request):
    return render(request, "dash_emp/dashboard.html")


class ResumeUploadView(View):

    def get(self, request):
        form = ResumeForm()
        return render(request, 'upload/resume.html', {
            'form': form
        })

    def post(self, request):
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save()
            resume_data = parse_resume(resume)
            return render(request, 'upload/resume.html', {
                'form': form,
                'resume_data': resume_data,
            })
        return render(request, 'upload/resume.html', {
            'form': form
        })

class VideoView(View):

    def get(self, request):
        return render(request, 'video/base.html')

class UserView(View):

    def get(self, request):
        return render(request, 'dash_emp/user.html')

    def post(self, request):
        post_data = request.POST
        print(post_data)
        return render(request, 'dash_emp/user.html')


class DashView(View):

    def get(self, request):
        return render(request, 'dash_emp/dashboard.html')

    def post(self, request):
        post_data = request.POST
        print(post_data)
        return render(request, 'dash_emp/dashboard.html')


def can_dash(request):
    return render(request, "dash_can/dashboard.html")


class CanUserView(View):

    def get(self, request):
        return render(request, 'dash_can/user.html')

    def post(self, request):
        post_data = request.POST
        print(post_data)
        return render(request, 'dash_can/user.html')


class CanEduView(View):

    def get(self, request):
        return render(request, 'dash_can/typography.html')

    def post(self, request):
        post_data = request.POST
        print(post_data)
        return render(request, 'dash_can/typography.html')

class CanWorkView(View):

    def get(self, request):
        return render(request, 'dash_can/icons.html')

    def post(self, request):
        post_data = request.POST
        print(post_data)
        return render(request, 'dash_can/icons.html')

class CanApplyView(View):

    def get(self, request):
        return render(request, 'dash_can/table.html')

    def post(self, request):
        post_data = request.POST
        print(post_data)
        return render(request, 'dash_can/table.html')
