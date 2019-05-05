from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [

    url(r'^signup/$', views.UserSignUpView.as_view(), name="user-signup"),
    url(r'^signup/recruiter/$', views.RecruiterSignUpView.as_view(), name="recruiter-signup"),

    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^dashboard/$', views.MyApplicationsView.as_view(), name='can_dash'),
    url(r'^dashboard/recruiter/$',views.dash_emp, name='dash'),
    url(r'^jobs/create/$', views.JobCreationView.as_view(), name='create-job'),
    url(r'^jobs/list/$', views.RecruiterManageJobsView.as_view(), name='recruiter-manage-jobs'),
    url(r'^jobs/(?P<job_id>[0-9]+)/update/$', views.JobUpdateView.as_view(), name='job-update'),
    url(r'^jobs/(?P<job_id>[0-9]+)/$', views.JobDetailView.as_view(), name='job-detail'),

    url(r'^jobs/list/relevant/$', views.RelevantJobsView.as_view(), name='relevant-jobs'),
    url(r'^jobs/(?P<job_id>[0-9]+)/apply/$', views.JobApplyView.as_view(), name='job-apply'),
    url(r'^jobs/(?P<job_id>[0-9]+)/resume/upload/$', views.JobResumeUploadView.as_view(), name='job-resume-upload'),
    url(r'^profile/$', views.CandidateProfileView.as_view(), name='profile'),
    path('experience/', views.ExperienceView.as_view(), name='experience'),
    path('experience/<int:exp_id>/delete', views.DeleteExperienceView.as_view(), name='delete-experience'),
    path('education/', views.EducationView.as_view(), name='education'),
    path('education/<int:edu_id>/delete', views.DeleteEducationView.as_view(), name='delete-education'),

    # url(r'^upload/resume/$', views.ResumeUploadView.as_view(), name="resume-upload"),
    url(r'^video/$', views.VideoView.as_view(), name="video"),

]