from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^signup/$', views.UserSignUpView.as_view(), name="user-signup"),
    url(r'^signup/recruiter/$', views.RecruiterSignUpView.as_view(), name="recruiter-signup"),

    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^dashboard/$', views.can_dash, name='can_dash'),
    url(r'^dashboard/recruiter/$',views.dash_emp, name='dash'),
    url(r'^jobs/create/$', views.JobCreationView.as_view(), name='create-job'),
    url(r'^jobs/list/$', views.RecruiterManageJobsView.as_view(), name='recruiter-manage-jobs'),
    url(r'^jobs/(?P<job_id>[0-9]+)/update/$', views.JobUpdateView.as_view(), name='job-update'),
    url(r'^jobs/(?P<job_id>[0-9]+)/$', views.JobDetailView.as_view(), name='job-detail'),

    url(r'^jobs/list/relevant/$', views.RelevantJobsView.as_view(), name='relevant-jobs'),
    url(r'^jobs/(?P<job_id>[0-9]+)/apply/$', views.JobApplyView.as_view(), name='job-apply'),
    url(r'^jobs/(?P<job_id>[0-9]+)/resume/upload/$', views.JobResumeUploadView.as_view(), name='job-resume-upload'),

    # url(r'^upload/resume/$', views.ResumeUploadView.as_view(), name="resume-upload"),
    url(r'^video/$', views.VideoView.as_view(), name="video"),

    url(r'^menuemp/$',views.menu_emp, name='menu_emp'),
    url(r'^user/$', views.UserView.as_view(), name='user'),


    url(r'^CanUserView/$', views.CanUserView.as_view(), name='CanUserView'),
    url(r'^CanEduView/$', views.CanEduView.as_view(), name='CanEduView'),
    url(r'^CanWorkView/$', views.CanWorkView.as_view(), name='CanWorkView'),
    url(r'^CanApplyView/$', views.CanApplyView.as_view(), name='CanApplyView'),

    #url(r'^agent-sign-up/', views.AgentSignUp.as_view(), name='agent-sign-up'),
    #url(r'^candidate-sign-up/', views.CandidateSignUp.as_view(), name='candidate-sign-up'),




]