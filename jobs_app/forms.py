from django import forms
from jobs_app.models import Signup, Signuprec, Resume


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





