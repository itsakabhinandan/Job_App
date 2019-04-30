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

    url(r'^upload/resume/$', views.ResumeUploadView.as_view(), name="resume-upload"),
    url(r'^video/$', views.VideoView.as_view(), name="video"),

    url(r'^menuemp/$',views.menu_emp, name='menu_emp'),
    url(r'^post_jobs/$', views.PostJobsView.as_view(), name='post_jobs'),
    url(r'^manage_jobs/$', views.ManageJobsView.as_view(), name='manage_jobs'),
    url(r'^user/$', views.UserView.as_view(), name='user'),


    url(r'^CanUserView/$', views.CanUserView.as_view(), name='CanUserView'),
    url(r'^CanEduView/$', views.CanEduView.as_view(), name='CanEduView'),
    url(r'^CanWorkView/$', views.CanWorkView.as_view(), name='CanWorkView'),
    url(r'^CanApplyView/$', views.CanApplyView.as_view(), name='CanApplyView'),

    #url(r'^agent-sign-up/', views.AgentSignUp.as_view(), name='agent-sign-up'),
    #url(r'^candidate-sign-up/', views.CandidateSignUp.as_view(), name='candidate-sign-up'),




]