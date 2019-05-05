import datetime

from django.conf import settings
from django.http import JsonResponse, Http404
from django.views import View
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404

from jobs_app.forms import ResumeForm, RecruiterCreationForm, JobForm, ExperienceForm, EducationForm
from jobs_app.models import Job, JobApplication, Resume, Experience

from jobs_app.forms import SignupForm, Signupformrec, LoginForm
from jobs_app.models import intro, Signup, Signuprec

from jobs_app.utils import parse_resume
from jobs_app.scoring import get_score_for_user_application
from jobs_app.update_profile import update_candidate_profile


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
        if request.user.is_authenticated:
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
        if request.user.is_authenticated:
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

    permission_required = ("can_create_job", )

    def get(self, request):
        jobs = request.user.job_set.all()
        print(jobs)
        for job in jobs:
            print(job.jobapplication_set.count())
        return render(request, 'dash_emp/manage_jobs.html', {
            'jobs': jobs
        })

class RelevantJobsView(LoginRequiredMixin, View):

    def get(self, request):
        jobs = Job.objects.filter(
            deadline__gte=datetime.datetime.now(),
        )
        return render(request, 'dash_can/relevant_jobs.html', {
            'jobs': jobs
        })

class JobApplyView(LoginRequiredMixin, View):

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        return render(request, 'dash_can/job_apply.html', {
            'job': job,
            'ziggeo_token': settings.ZIGGEO_TOKEN
        })
    
    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        data = request.POST
        if data.get('form_type') == 'resume-upload':
            form = ResumeForm(request.POST, request.FILES)
            if form.is_valid():
                resume = form.save()
                resume_data = parse_resume(resume)
                return render(request, 'dash_can/job_apply.html', {
                    'job': job,
                    'resume': resume,
                    'ziggeo_token': settings.ZIGGEO_TOKEN,
                    'resume_data': resume_data,
                })
            return render(request, 'dash_can/job_apply.html', {
                'job': job,
                'ziggeo_token': settings.ZIGGEO_TOKEN,
                'resume_data': {}
            })
        
        elif data.get('form_type') == 'apply':
            # check data and save the application
            try:
                application = JobApplication.objects.get(
                    user=request.user,
                    job=job,
                )
                return redirect('can_dash')
            except JobApplication.DoesNotExist:
                pass

            required_fields = ['name', 'email', 'cover_letter']
            if all(field in request.POST for field in required_fields):
                resume = None
                if request.POST.get('resume_id', None):
                    resume = Resume.objects.get(
                        id=int(request.POST.get('resume_id'))
                    )
                application = JobApplication(
                    user=request.user,
                    job=job,
                    resume=resume,
                    name=request.POST.get('name'),
                    email=request.POST.get('email'),
                    cover_letter=request.POST.get('cover_letter'),
                    sites=','.join(request.POST.getlist('sites[]', [])),
                    skills=','.join(request.POST.getlist('skills[]', [])),
                    video_token=request.POST.get('video_token', '')
                )
                score = get_score_for_user_application(request.user, application)
                application.score = score
                application.save()
                update_candidate_profile(request.user, application)
                return redirect('profile')
            return render(request, 'dash_can/job_apply.html', {
                'job': job,
                'ziggeo_token': settings.ZIGGEO_TOKEN,
                'resume_data': {}
            })
        
        return render(request, 'dash_can/job_apply.html', {
            'job': job,
            'ziggeo_token': settings.ZIGGEO_TOKEN,
            'resume_data': {}
        })


class MyApplicationsView(LoginRequiredMixin, View):

    def get(self, request):
        job_applications = request.user.jobapplication_set.all()
        return render(request, 'dash_can/my_applications.html', {
            'job_applications': job_applications,
        })


class CandidateProfileView(LoginRequiredMixin, View):

    def get(self, request):
        skills = []
        if request.user.candidateprofile.skills:
            skills = request.user.candidateprofile.skills.split(',')
        return render(request, 'dash_can/profile.html', {
            'skills': skills
        })
    
    def post(self, request):
        data = request.POST
        request.user.first_name = data.get('first_name', '')
        request.user.last_name = data.get('last_name', '')
        request.user.candidateprofile.name = '{0} {1}'.format(data.get('first_name', ''), data.get('last_name', ''))
        request.user.candidateprofile.gender = data.get('gender', '')
        request.user.candidateprofile.address = data.get('address', '')
        request.user.candidateprofile.city = data.get('city', '')
        request.user.candidateprofile.country = data.get('country', '')
        request.user.candidateprofile.phone = data.get('phone', '')
        request.user.candidateprofile.postal_code = data.get('postal_code', '')
        request.user.candidateprofile.about = data.get('about', '')

        request.user.candidateprofile.skills = ','.join(data.getlist("skills[]", []))

        request.user.save()
        request.user.candidateprofile.save()

        skills = []
        if request.user.candidateprofile.skills:
            skills = request.user.candidateprofile.skills.split(',')

        return render(request, 'dash_can/profile.html', {
            'skills': skills
        })


class ExperienceView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'dash_can/work_details.html')

    def post(self, request):
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            return render(request, 'dash_can/work_details.html')
        print(form)
        return render(request, 'dash_can/work_details.html')


class DeleteExperienceView(LoginRequiredMixin, View):

    def get(self, request, exp_id):
        try:
            exp = request.user.experience_set.get(id=exp_id)
            exp.delete()
            return redirect('experience')
        except Experience.DoesNotExist:
            raise Http404()

class EducationView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'dash_can/education.html')
    
    def post(self, request):
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = request.user
            education.save()
            return render(request, 'dash_can/education.html')
        return render(request, 'dash_can/education.html')

class DeleteEducationView(LoginRequiredMixin, View):

    def get(self, request, edu_id):
        try:
            exp = request.user.education_set.get(id=edu_id)
            exp.delete()
            return redirect('education')
        except Experience.DoesNotExist:
            raise Http404()

class ListApplicationsView(PermissionRequiredMixin, LoginRequiredMixin, View):

    permission_required = ('can_access_recruiter_dashboard', )

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        applications = job.jobapplication_set.all().order_by('-score')
        return render(request, 'dash_emp/list_application.html', {
            'applications': applications
        })

class ApplicationView(PermissionRequiredMixin, LoginRequiredMixin, View):

    permission_required = ('can_access_recruiter_dashboard', )

    def get(self, request, job_id, app_id):
        application = get_object_or_404(JobApplication, id=app_id)
        return render(request, 'dash_emp/application.html', {
            'application': application,
            'ziggeo_token': settings.ZIGGEO_TOKEN,
            'skills': application.skills.split(','),
            'sites': application.sites.split(','),
        })


class JobResumeUploadView(View):
    """
    This view is not in use
    """

    def post(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save()
            resume_data = parse_resume(resume)
            return render(request, 'dash_can/job_apply.html', {
                'job': job,
                'resume_data': resume_data,
            })
        return render(request, 'upload/job_apply.html.html', {
            'job': job,
            'resume_data': {}
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

def can_dash(request):
    return render(request, "dash_can/dashboard.html")

class RecruiterDashboard(PermissionRequiredMixin, LoginRequiredMixin, View):

    permission_required = ('can_access_recruiter_dashboard', )

    def get(self, request):
        return render(request, 'dash_emp/dashboard.html')