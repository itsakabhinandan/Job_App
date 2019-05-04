from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from jobs_app.models import Signup, Signuprec, Resume, Job, Experience


class RecruiterCreationForm(UserCreationForm):
    designation = forms.CharField()
    company = forms.CharField()
    office_address = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username', 'designation', 'company', 'office_address', 'email', 'password1', 'password2')

class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ('title', 'description', 'category', 'experience', 'type', 'qualification', 'deadline')

class ExperienceForm(forms.ModelForm):

    class Meta:
        model = Experience
        fields = ('title', 'description')


class SignupForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
    cpassword = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = Signup
        fields = ['username', 'password', 'cpassword']


class Signupformrec(forms.ModelForm):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
    cpassword = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = Signuprec
        fields = ['username', 'password', 'cpassword']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=10, widget=forms.PasswordInput)


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('resume', )





