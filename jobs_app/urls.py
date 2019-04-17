from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^signrec/$',views.sign_rec, name='sign_rec'),
    url(r'^signcan/$',views.sign_can, name='sign_can'),
    url(r'^menuemp/$',views.menu_emp, name='menu_emp'),
    url(r'^dashemp/$',views.dash_emp, name='dash_emp'),

    url(r'^upload/resume/$', views.ResumeUploadView.as_view(), name="resume-upload")

    #url(r'^agent-sign-up/', views.AgentSignUp.as_view(), name='agent-sign-up'),
    #url(r'^candidate-sign-up/', views.CandidateSignUp.as_view(), name='candidate-sign-up'),




]