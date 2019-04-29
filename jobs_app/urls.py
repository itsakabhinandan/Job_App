from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^signrec/$',views.sign_rec, name='sign_rec'),
    url(r'^signcan/$',views.sign_can, name='sign_can'),
    url(r'^menuemp/$',views.menu_emp, name='menu_emp'),
    url(r'^dashemp/$',views.dash_emp, name='dash'),

    url(r'^upload/resume/$', views.ResumeUploadView.as_view(), name="resume-upload"),
    url(r'^video/$', views.VideoView.as_view(), name="video"),

    url(r'^post_jobs/$', views.PostJobsView.as_view(), name='post_jobs'),
    url(r'^manage_jobs/$', views.ManageJobsView.as_view(), name='manage_jobs'),
    url(r'^user/$', views.UserView.as_view(), name='user'),


    url(r'^can_dash/$', views.can_dash, name='can_dash'),
    url(r'^CanUserView/$', views.CanUserView.as_view(), name='CanUserView'),
    url(r'^CanEduView/$', views.CanEduView.as_view(), name='CanEduView'),
    url(r'^CanWorkView/$', views.CanWorkView.as_view(), name='CanWorkView'),
    url(r'^CanApplyView/$', views.CanApplyView.as_view(), name='CanApplyView'),

    #url(r'^agent-sign-up/', views.AgentSignUp.as_view(), name='agent-sign-up'),
    #url(r'^candidate-sign-up/', views.CandidateSignUp.as_view(), name='candidate-sign-up'),




]