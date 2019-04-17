from django.views import View
from django.shortcuts import render, redirect

from jobs_app.forms import ResumeForm

from jobs_app.forms import SignupForm, Signupformrec, LoginForm
from jobs_app.models import intro, Signup, Signuprec

from jobs_app.utils import parse_resume


def sign_can(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            a = request.POST['first_name']
            b = request.POST['last_name']
            c = request.POST['email']
            un = form.cleaned_data['username']
            p = form.cleaned_data['password']
            cp = form.cleaned_data['cpassword']

            if p == cp:
                s = Signup()
                s.first_name = a
                s.last_name = b
                s.email = c
                s.username = un
                s.password = p
                s.cpassword = cp
                s.save()
                context = {
                    'form': form,
                    'data': 'data is saved'
                }
                return render(request, 'login/login.html', context)
            else:
                form = SignupForm()
                context = {
                    'form': form,
                    'data': 'password is not same'
                }
                return render(request, 'sign_can/sign_can.html', context)
        else:
            form = SignupForm()
            return render(request, 'sign_can/sign_can.html', {'form': form})
    return render(request, 'sign_can/sign_can.html', {'form': form})


def sign_rec(request):
    form = Signupformrec()
    if request.method == 'POST':
        form = Signupformrec(request.POST)
        if form.is_valid():
            a = request.POST['first_name']
            b = request.POST['last_name']
            c = request.POST['email']
            d = request.POST['designation']
            e = request.POST['company']
            f = request.POST['office_ad']
            un = form.cleaned_data['username']
            p = form.cleaned_data['password']
            cp = form.cleaned_data['cpassword']

            if p == cp:
                s = Signuprec()
                s.first_name = a
                s.last_name = b
                s.email = c
                s.designation = d
                s.company = e
                s.office_ad = f
                s.username = un
                s.password = p
                s.cpassword = cp
                s.save()
                context = {
                    'form': form,
                    'data': 'data is saved'
                }
                return render(request, 'login/login.html', context)
            else:
                form = Signupformrec()
                context = {
                    'form': form,
                    'data': 'password is not same'
                }
                return render(request, 'sign_rec/sign_rec.html', context)
        else:
            form = Signupformrec()
            return render(request, 'sign_rec/sign_rec.html', {'form': form})
    return render(request, 'sign_rec/sign_rec.html', {'form': form})


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





def sign_rec(request):
    return render(request, "sign_rec/sign_rec.html")


# def sign_can(request):
# return render(request, "sign_can/sign_can.html")


def menu_emp(request):
    return render(request, "menu_emp/menu_emp.html")


def menu_can(request):
    return render(request, "menu_can/menu_can.html")


def dash_emp(request):
    return render(request, "dash_emp/dashboard.html")


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            s = Signup.objects.filter(username=u)
            if len(s) > 0:
                s = s[0]
                du = s.username
                dp = s.password
                if u == du and p == dp:
                    request.session['username'] = u
                    context = {
                        'username': u,
                        'data ':' you are logged in'
                    }
                    return render(request, 'dash_emp/dashboard.html', context)
                else:
                    form = LoginForm()
                    context = {
                        'form': form,
                        'data': 'wrong username and password'
                    }
                    return render(request, 'login/login.html', context)
            else:
                form = LoginForm()
                context = {
                    'form':form,
                    'data':'data not found'
                }
                return render(request, 'login/login.html', context)
    elif request.method == 'GET':
        if 'user' in request.GET:
            if request.session.has_key('username'):
                request.session.flush()
        if request.session.has_key('username'):
            user_data=request.session['username']
            context={'user_data':user_data,
                     'data':'hello you are logged in'}
            return render(request, 'dash_emp/dashboard.html', context)
        else:
            return render(request,'login/login.html', {'form': form})


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